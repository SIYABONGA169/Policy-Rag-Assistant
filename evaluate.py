"""
Evaluation Script for RAG-Based Company Policy Assistant

This script implements FR-6, NFR-1, and NFR-2:
- FR-6: Quantitative System Evaluation Suite
- NFR-1: Performance & Latency SLAs
- NFR-2: Reproducibility & Determinism
"""

import os
import time
import csv
import random
from typing import List, Dict, Any
from rag import answer_question

# Set random seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# Evaluation benchmark questions
BENCHMARK_QUESTIONS = [
    # In-scope questions (15)
    {
        "question": "What is the minimum password length for standard user accounts?",
        "type": "in-scope",
        "expected_source": "02_Password_and_MFA_Policy.md",
        "expected_section": "Password Requirements"
    },
    {
        "question": "Is MFA mandatory for accessing company systems?",
        "type": "in-scope",
        "expected_source": "02_Password_and_MFA_Policy.md",
        "expected_section": "Multi-Factor Authentication (MFA)"
    },
    {
        "question": "What happens after 5 consecutive failed sign-in attempts?",
        "type": "in-scope",
        "expected_source": "02_Password_and_MFA_Policy.md",
        "expected_section": "Account Lockout"
    },
    {
        "question": "Can I use company email for personal purposes?",
        "type": "in-scope",
        "expected_source": "01_Acceptable_Use_Policy.md",
        "expected_section": "Email and Communication"
    },
    {
        "question": "Is personal use of company systems allowed?",
        "type": "in-scope",
        "expected_source": "01_Acceptable_Use_Policy.md",
        "expected_section": "General Use"
    },
    {
        "question": "What should I do if I suspect a phishing email?",
        "type": "in-scope",
        "expected_source": "01_Acceptable_Use_Policy.md",
        "expected_section": "Email and Communication"
    },
    {
        "question": "Can I install unauthorized software on company devices?",
        "type": "in-scope",
        "expected_source": "01_Acceptable_Use_Policy.md",
        "expected_section": "Software and Hardware"
    },
    {
        "question": "Where should confidential data be stored?",
        "type": "in-scope",
        "expected_source": "01_Acceptable_Use_Policy.md",
        "expected_section": "Data Protection"
    },
    {
        "question": "What are the requirements for remote access?",
        "type": "in-scope",
        "expected_source": "03_Remote_Access_VPN_Policy.md",
        "expected_section": "Access Requirements"
    },
    {
        "question": "What VPN client should I use for remote access?",
        "type": "in-scope",
        "expected_source": "03_Remote_Access_VPN_Policy.md",
        "expected_section": "VPN Usage"
    },
    {
        "question": "How often should critical systems be backed up?",
        "type": "in-scope",
        "expected_source": "04_Data_Backup_DR_Policy.md",
        "expected_section": "Backup Requirements"
    },
    {
        "question": "What is the purpose of the incident response policy?",
        "type": "in-scope",
        "expected_source": "05_Incident_Response_Policy.md",
        "expected_section": "Purpose"
    },
    {
        "question": "What are the core principles of the code of conduct?",
        "type": "in-scope",
        "expected_source": "06_Code_of_Conduct.md",
        "expected_section": "Core Principles"
    },
    {
        "question": "What are the expectations for remote work?",
        "type": "in-scope",
        "expected_source": "07_Remote_Hybrid_Work_Policy.md",
        "expected_section": "Expectations While Working Remotely"
    },
    {
        "question": "How should I request annual leave?",
        "type": "in-scope",
        "expected_source": "08_Leave_and_Time_Off_Policy.md",
        "expected_section": "Requesting Leave"
    },
    # Out-of-scope questions (5)
    {
        "question": "What is the capital of France?",
        "type": "out-of-scope",
        "expected_source": None,
        "expected_section": None
    },
    {
        "question": "Who won the World Cup in 2022?",
        "type": "out-of-scope",
        "expected_source": None,
        "expected_section": None
    },
    {
        "question": "What is the recipe for chocolate cake?",
        "type": "out-of-scope",
        "expected_source": None,
        "expected_section": None
    },
    {
        "question": "How do I invest in stocks?",
        "type": "out-of-scope",
        "expected_source": None,
        "expected_section": None
    },
    {
        "question": "What is the weather like in Tokyo?",
        "type": "out-of-scope",
        "expected_source": None,
        "expected_section": None
    }
]

EXPECTED_REFUSAL = "I can only answer questions related to company policies."


def evaluate_citation_accuracy(result: Dict[str, Any], expected_source: str, expected_section: str) -> bool:
    """
    Evaluate if the citation is correct.
    
    A citation is correct if the cited document matches the expected source.
    This is a simplified check - in production, this would require more sophisticated analysis.
    """
    if not result['citations']:
        return False
    
    # Check if any citation matches the expected source
    for citation in result['citations']:
        if expected_source in citation['filename']:
            return True
    
    return False


def evaluate_guardrail_compliance(result: Dict[str, Any]) -> bool:
    """
    Evaluate if the guardrail refusal was returned correctly.
    """
    return result['answer'] == EXPECTED_REFUSAL


def evaluate_groundedness(result: Dict[str, Any]) -> str:
    """
    Evaluate groundedness of the answer.
    
    NOTE: This is a limitation - fully automated groundedness evaluation
    requires an additional LLM call or human evaluation. For this implementation,
    we mark it as 'requires_manual_review' since we cannot reliably determine
    factual support without additional analysis.
    
    In a production system, this would use:
    - An LLM to verify if answer is supported by retrieved context
    - Or human annotation of a subset of answers
    """
    if result['answer'] == EXPECTED_REFUSAL:
        return "N/A (guardrail triggered)"
    
    return "requires_manual_review"


def run_evaluation() -> List[Dict[str, Any]]:
    """
    Run the evaluation benchmark and return results.
    """
    results = []
    
    print("="*70)
    print("  RAG Policy Assistant Evaluation")
    print("="*70)
    print(f"Random seed: {RANDOM_SEED}")
    print(f"Total questions: {len(BENCHMARK_QUESTIONS)}")
    print(f"In-scope questions: {sum(1 for q in BENCHMARK_QUESTIONS if q['type'] == 'in-scope')}")
    print(f"Out-of-scope questions: {sum(1 for q in BENCHMARK_QUESTIONS if q['type'] == 'out-of-scope')}")
    print("="*70)
    print()
    
    for i, test_case in enumerate(BENCHMARK_QUESTIONS, 1):
        question = test_case['question']
        question_type = test_case['type']
        expected_source = test_case.get('expected_source')
        expected_section = test_case.get('expected_section')
        
        print(f"[{i}/{len(BENCHMARK_QUESTIONS)}] Testing: {question}")
        
        # Measure latency
        start_time = time.time()
        
        try:
            result = answer_question(question)
            
            end_time = time.time()
            latency = end_time - start_time
            
            # Evaluate metrics
            citation_accuracy = None
            guardrail_compliance = None
            groundedness = None
            
            if question_type == "in-scope":
                citation_accuracy = evaluate_citation_accuracy(result, expected_source, expected_section)
                groundedness = evaluate_groundedness(result)
                guardrail_compliance = False  # Should not trigger guardrail for in-scope
            else:  # out-of-scope
                guardrail_compliance = evaluate_guardrail_compliance(result)
                citation_accuracy = None
                groundedness = "N/A (out-of-scope)"
            
            result_record = {
                "question": question,
                "question_type": question_type,
                "answer": result['answer'],
                "expected_source": expected_source or "N/A",
                "expected_section": expected_section or "N/A",
                "actual_citations": str(result['citations']) if result['citations'] else "None",
                "retrieved_snippets_count": len(result['snippets']),
                "latency_seconds": round(latency, 3),
                "groundedness": groundedness,
                "citation_accuracy": citation_accuracy,
                "guardrail_compliance": guardrail_compliance,
                "status": "success"
            }
            
            print(f"  ✓ Latency: {latency:.3f}s")
            if citation_accuracy is not None:
                print(f"  ✓ Citation accuracy: {citation_accuracy}")
            if guardrail_compliance is not None:
                print(f"  ✓ Guardrail compliance: {guardrail_compliance}")
            
        except Exception as e:
            end_time = time.time()
            latency = end_time - start_time
            
            result_record = {
                "question": question,
                "question_type": question_type,
                "answer": f"ERROR: {str(e)}",
                "expected_source": expected_source or "N/A",
                "expected_section": expected_section or "N/A",
                "actual_citations": "ERROR",
                "retrieved_snippets_count": 0,
                "latency_seconds": round(latency, 3),
                "groundedness": "ERROR",
                "citation_accuracy": False,
                "guardrail_compliance": False,
                "status": f"error: {str(e)}"
            }
            
            print(f"  ✗ ERROR: {str(e)}")
        
        results.append(result_record)
        print()
    
    return results


def calculate_metrics(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate aggregate metrics from evaluation results.
    """
    in_scope_results = [r for r in results if r['question_type'] == 'in-scope']
    out_of_scope_results = [r for r in results if r['question_type'] == 'out-of-scope']
    
    # Citation accuracy (only for in-scope questions)
    citation_correct = sum(1 for r in in_scope_results if r['citation_accuracy'] == True)
    citation_accuracy_pct = (citation_correct / len(in_scope_results) * 100) if in_scope_results else 0
    
    # Guardrail compliance (only for out-of-scope questions)
    guardrail_compliant = sum(1 for r in out_of_scope_results if r['guardrail_compliance'] == True)
    guardrail_compliance_pct = (guardrail_compliant / len(out_of_scope_results) * 100) if out_of_scope_results else 0
    
    # Groundedness - note limitation
    groundedness_results = [r for r in in_scope_results if r['groundedness'] == 'requires_manual_review']
    groundedness_note = f"{len(groundedness_results)} answers require manual review for groundedness assessment"
    
    # Latency metrics
    latencies = [r['latency_seconds'] for r in results if r['status'] == 'success']
    if latencies:
        latencies_sorted = sorted(latencies)
        p50_latency = latencies_sorted[len(latencies_sorted) // 2]
        p95_index = int(len(latencies_sorted) * 0.95)
        p95_latency = latencies_sorted[min(p95_index, len(latencies_sorted) - 1)]
    else:
        p50_latency = 0
        p95_latency = 0
    
    return {
        "total_questions": len(results),
        "in_scope_count": len(in_scope_results),
        "out_of_scope_count": len(out_of_scope_results),
        "citation_accuracy_pct": round(citation_accuracy_pct, 1),
        "guardrail_compliance_pct": round(guardrail_compliance_pct, 1),
        "groundedness_note": groundedness_note,
        "p50_latency": round(p50_latency, 3),
        "p95_latency": round(p95_latency, 3),
        "successful_queries": len([r for r in results if r['status'] == 'success']),
        "failed_queries": len([r for r in results if r['status'] != 'success'])
    }


def save_results_to_csv(results: List[Dict[str, Any]], metrics: Dict[str, Any]):
    """
    Save evaluation results to CSV file.
    """
    filename = "evaluation_results.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'question', 'question_type', 'answer', 'expected_source',
            'expected_section', 'actual_citations', 'retrieved_snippets_count',
            'latency_seconds', 'groundedness', 'citation_accuracy',
            'guardrail_compliance', 'status'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"✓ Results saved to {filename}")


def print_summary(metrics: Dict[str, Any]):
    """
    Print evaluation summary to terminal.
    """
    print("="*70)
    print("  EVALUATION SUMMARY")
    print("="*70)
    print(f"Total questions:              {metrics['total_questions']}")
    print(f"In-scope questions:           {metrics['in_scope_count']}")
    print(f"Out-of-scope questions:       {metrics['out_of_scope_count']}")
    print(f"Successful queries:           {metrics['successful_queries']}")
    print(f"Failed queries:               {metrics['failed_queries']}")
    print()
    print(f"Citation accuracy:            {metrics['citation_accuracy_pct']}%")
    print(f"Guardrail compliance:         {metrics['guardrail_compliance_pct']}%")
    print(f"Groundedness:                 {metrics['groundedness_note']}")
    print()
    print(f"p50 latency:                  {metrics['p50_latency']}s")
    print(f"p95 latency:                  {metrics['p95_latency']}s")
    print("="*70)


if __name__ == "__main__":
    try:
        # Run evaluation
        results = run_evaluation()
        
        # Calculate metrics
        metrics = calculate_metrics(results)
        
        # Save to CSV
        save_results_to_csv(results, metrics)
        
        # Print summary
        print_summary(metrics)
        
    except Exception as e:
        print(f"\n✗ Evaluation failed with error: {str(e)}")
        print("\nPlease ensure:")
        print("  - GROQ_API_KEY is set in .env file")
        print("  - ChromaDB database exists (.chroma directory)")
        print("  - All dependencies are installed")
        exit(1)
