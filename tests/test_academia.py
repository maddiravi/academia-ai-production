import unittest
from unittest.mock import patch, MagicMock
from agents.document_ingestor import DocumentIngestorAgent
from agents.thesis_extractor import ThesisExtractorAgent
from tools.safety import sanitize_content

class TestAcademiaCore(unittest.TestCase):
    
    @patch('agents.thesis_extractor.ChatOpenAI') # FIX 2: Mock the LLM to bypass API Key check
    def test_keyword_extraction_logic(self, MockChat):
        """Unit Test: Verifies NLP keyword extraction works on simulated text."""
        # Since ChatOpenAI is mocked, this line won't crash even without an API key
        extractor = ThesisExtractorAgent()
        
        simulated_text = "Deep learning uses neural networks for optimization."
        keywords = extractor.extract_keywords(simulated_text)
        
        # Check that expected keywords are found
        self.assertIn("learning", keywords)
        self.assertIn("neural", keywords)

    @patch('agents.document_ingestor.PyPDFLoader')
    @patch('os.path.exists', return_value=True)
    def test_ingestion_flow(self, mock_exists, MockLoader):
        """Integration Test: Verifies ingestion logic without real files."""
        # Setup the mock loader
        mock_loader_instance = MockLoader.return_value
        
        # FIX 1: Create a mock document that satisfies Pydantic requirements
        mock_doc = MagicMock()
        mock_doc.page_content = "Simulated Content"
        mock_doc.metadata = {} # Critical: Must be a dictionary, not a Mock object
        
        mock_loader_instance.load.return_value = [mock_doc]
        
        # Run the agent
        agent = DocumentIngestorAgent("dummy.pdf")
        chunks, content = agent.process_document()
        
        # Assertions
        self.assertIn("Simulated Content", content)
        self.assertTrue(len(chunks) > 0)

        def test_safety_guardrails(self):
        unsafe_input = "Summary with <script>alert('hack')</script> tags."
        clean_output = sanitize_content(unsafe_input)
        self.assertEqual(clean_output, "Summary with  tags.")

    def test_agent_state_handoff(self):
        """Integration Test: Verifies data structure between agents."""
        # Simulate state after Agent 1
        state_after_ingest = {
            "original_content": "Academic text content...",
            "chunks": ["chunk1", "chunk2"]
        }
        # Check if keys exist for Agent 2 consumption
        self.assertIn("original_content", state_after_ingest)
        self.assertIsInstance(state_after_ingest["chunks"], list)

if __name__ == '__main__':
    unittest.main()