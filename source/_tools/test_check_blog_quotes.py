import unittest

from source._tools.check_blog_quotes import build_run_index, iter_runs


class BlogQuoteRunIndexTest(unittest.TestCase):
    def test_iter_runs_uses_precomputed_blog_runs(self):
        blog_runs = build_run_index("abcdefg", 3)

        self.assertEqual(list(iter_runs(blog_runs, "xxabcdeyy", 3)), ["abc", "bcd", "cde"])


if __name__ == "__main__":
    unittest.main()
