"""Tests for the deterministic outline builders; no credentials or network needed."""
import unittest

from bot.services.outlines import make_presentation_outline, make_work_outline


class OutlineTests(unittest.TestCase):
    def test_work_outline_includes_requested_details_and_disclaimer(self):
        result = make_work_outline({
            "kind": "Реферат", "topic": "Вода", "subject": "Биология",
            "volume": "5 страниц", "language": "Русский", "requirements": "2 главы",
            "sources": "Да",
        })
        for expected in ("Реферат", "Вода", "Биология", "5 страниц", "2 главы", "Источники", "не готовая академическая работа"):
            self.assertIn(expected, result)

    def test_presentation_outline_has_requested_number_of_slides(self):
        result = make_presentation_outline({
            "topic": "Космос", "slides": "6", "language": "Русский", "style": "Академический"
        })
        self.assertEqual(sum(1 for line in result.splitlines() if line.startswith("Слайд ")), 6)
        self.assertIn("Космос", result)
        self.assertIn("PPTX пока не создаётся", result)

    def test_presentation_slide_count_is_bounded(self):
        result = make_presentation_outline({
            "topic": "Тема", "slides": "100", "language": "English", "style": "Minimal"
        })
        self.assertEqual(sum(1 for line in result.splitlines() if line.startswith("Слайд ")), 20)


if __name__ == "__main__":
    unittest.main()
