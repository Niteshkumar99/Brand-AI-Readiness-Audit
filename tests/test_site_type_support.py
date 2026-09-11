import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_module(name, relative_path):
    module_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


run_audit = load_module("run_audit", "skills/audit-orchestrator/scripts/run_audit.py")
engagement_check = load_module("engagement_check", "skills/engagement-orientation-audit/scripts/engagement_check.py")


class SiteTypeSupportTests(unittest.TestCase):
    def test_cli_accepts_site_type_hint(self):
        cfg = run_audit.parse_cli_args(["https://shop.example.com", "--site-type", "ecommerce"])
        self.assertEqual(cfg["site_type"], "ecommerce")

    def test_auto_detects_site_type_from_domain(self):
        self.assertEqual(run_audit.detect_site_type("https://shop.example.com"), "ecommerce")
        self.assertEqual(run_audit.detect_site_type("https://docs.example.com"), "docs")
        self.assertEqual(run_audit.detect_site_type("https://app.example.com"), "saas")
        self.assertEqual(run_audit.detect_site_type("https://enterprise.example.com"), "enterprise")

    def test_docs_cta_keywords_include_docs_terms(self):
        keywords = engagement_check.get_cta_keywords("docs")
        self.assertTrue(any(term in keywords for term in ["docs", "api", "guide", "tutorial"]))

    def test_ecommerce_cta_keywords_include_store_terms(self):
        keywords = engagement_check.get_cta_keywords("ecommerce")
        self.assertTrue(any(term in keywords for term in ["shop now", "pricing", "buy", "checkout"]))


if __name__ == "__main__":
    unittest.main()
