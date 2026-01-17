import requests
import time

def evaluate_system():
    # UPDATED: Test cases matching the new 10-document dataset
    test_set = [
        {
            "query": "What are the latest trends in AI?",
            "expected_doc": "doc_0_AI_Trends.pdf" 
        },
        {
            "query": "I need information about Supply Chain growth.",
            "expected_doc": "doc_2_Supply_Chain.pdf"
        },
        {
            "query": "Show me the report on Legal Disclaimers.",
            "expected_doc": "doc_text_only_1.pdf"
        },
        {
            "query": "What does the Marketing analysis show?",
            "expected_doc": "doc_4_Marketing.pdf"
        },
        # This query targets the standalone image we created
        {
            "query": "A pie chart with yellow and green slices",
            "expected_doc": "standalone_diagram_0.jpg"
        }
    ]

    print(f"📉 Starting Evaluation on {len(test_set)} test queries...\n")
    
    hits = 0
    total_time = 0

    for item in test_set:
        query = item["query"]
        expected = item["expected_doc"]
        
        start_time = time.time()
        
        try:
            # Call your API
            response = requests.post(
                "http://127.0.0.1:8000/query",
                json={"query": query}
            )
            result = response.json()
            
            # Measure Latency
            latency = time.time() - start_time
            total_time += latency

            # Check for Hit (Did we find the right document?)
            found_sources = [s['document_id'] for s in result.get('sources', [])]
            
            # Check if expected document is in the top results
            is_hit = expected in found_sources
            
            if is_hit:
                hits += 1
                status = "✅ PASS"
            else:
                status = "❌ FAIL"

            print(f"{status} | Query: '{query}'")
            print(f"   -> Latency: {latency:.2f}s")
            print(f"   -> Expected: {expected} | Found: {found_sources}")
            print("-" * 40)

        except Exception as e:
            print(f"⚠️ Error querying API: {e}")

    # Calculate Metrics
    if len(test_set) > 0:
        hit_rate = hits / len(test_set)
        avg_latency = total_time / len(test_set)

        print("\n📊 FINAL METRICS")
        print(f"Hit Rate: {hit_rate * 100:.1f}%")
        print(f"Avg Latency: {avg_latency:.2f} seconds")
        
        if hit_rate >= 0.8:
            print("\n🏆 RESULT: PASSED (System is retrieving correctly)")
        else:
            print("\n⚠️ RESULT: NEEDS IMPROVEMENT")

if __name__ == "__main__":
    evaluate_system()