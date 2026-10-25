"""
Test script for RAG pipeline (Stage 3)

Tests:
- Test A: Policy question
- Test B: Out-of-scope question
- Test C: Empty question
"""

import os
from rag import answer_question


def print_test_header(test_name: str):
    """Print a formatted test header."""
    print("\n" + "="*70)
    print(f"  {test_name}")
    print("="*70)


def test_policy_question():
    """Test A: Policy-related question."""
    print_test_header("Test A: Policy Question")
    
    query = "What is the acceptable use policy for company systems?"
    print(f"Query: {query}\n")
    
    result = answer_question(query)
    
    print(f"Answer: {result['answer']}\n")
    print(f"Citations ({len(result['citations'])}):")
    for citation in result['citations']:
        print(f"  - File: {citation['filename']}")
        print(f"    Section: {citation['section']}")
    print(f"\nSnippets ({len(result['snippets'])}):")
    for i, snippet in enumerate(result['snippets'], 1):
        print(f"  {i}. {snippet[:150]}...")
    
    # Verify expected structure
    assert 'answer' in result, "Missing 'answer' in result"
    assert 'citations' in result, "Missing 'citations' in result"
    assert 'snippets' in result, "Missing 'snippets' in result"
    assert isinstance(result['citations'], list), "Citations should be a list"
    assert isinstance(result['snippets'], list), "Snippets should be a list"
    
    print("\n✓ Test A passed")


def test_out_of_scope_question():
    """Test B: Out-of-scope question."""
    print_test_header("Test B: Out-of-Scope Question")
    
    query = "What is the capital of France?"
    print(f"Query: {query}\n")
    
    result = answer_question(query)
    
    print(f"Answer: {result['answer']}\n")
    print(f"Citations: {result['citations']}")
    print(f"Snippets: {result['snippets']}")
    
    # Verify exact refusal message
    expected_refusal = "I can only answer questions related to company policies and procedures."
    assert result['answer'] == expected_refusal, f"Expected exact refusal, got: {result['answer']}"
    assert result['citations'] == [], "Citations should be empty for out-of-scope"
    assert result['snippets'] == [], "Snippets should be empty for out-of-scope"
    
    print("\n✓ Test B passed")


def test_empty_question():
    """Test C: Empty question."""
    print_test_header("Test C: Empty Question")
    
    query = ""
    print(f"Query: '{query}'\n")
    
    result = answer_question(query)
    
    print(f"Answer: {result['answer']}\n")
    print(f"Citations: {result['citations']}")
    print(f"Snippets: {result['snippets']}")
    
    # Verify refusal for empty query
    expected_refusal = "I can only answer questions related to company policies and procedures."
    assert result['answer'] == expected_refusal, f"Expected refusal for empty query, got: {result['answer']}"
    
    print("\n✓ Test C passed")


def test_whitespace_only_question():
    """Test C variant: Whitespace-only question."""
    print_test_header("Test C Variant: Whitespace-Only Question")
    
    query = "   "
    print(f"Query: '{query}'\n")
    
    result = answer_question(query)
    
    print(f"Answer: {result['answer']}\n")
    
    # Verify refusal for whitespace-only query
    expected_refusal = "I can only answer questions related to company policies and procedures."
    assert result['answer'] == expected_refusal, f"Expected refusal for whitespace query, got: {result['answer']}"
    
    print("\n✓ Test C variant passed")


if __name__ == "__main__":
    # Check for Groq API key
    if not os.getenv("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY not found in environment variables.")
        print("Please set it in your .env file or environment before running tests.")
        exit(1)
    
    try:
        test_policy_question()
        test_out_of_scope_question()
        test_empty_question()
        test_whitespace_only_question()
        
        print("\n" + "="*70)
        print("  ALL TESTS PASSED")
        print("="*70 + "\n")
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        exit(1)
