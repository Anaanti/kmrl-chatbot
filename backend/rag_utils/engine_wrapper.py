# backend/rag_utils/engine_wrapper.py

_answer_query = None

def get_answer_query_func():
    """Returns the answer_query function, importing it only once (lazy import)."""
    global _answer_query
    if _answer_query is None:
        # This dynamic import prevents the slow code in query_llm.py from running on Django startup
        from .query_llm import answer_query
        _answer_query = answer_query
    return _answer_query

# This is the function the Django view will actually call
def ask_rag_engine(user_query, top_k=5):
    """The function exposed to the API view."""
    answer_query_func = get_answer_query_func()
    if answer_query_func:
        # The first time this runs, it will load the LLM.
        return answer_query_func(user_query, top_k)
    return {"answer": "Error: RAG engine failed to load.", "sources": []}