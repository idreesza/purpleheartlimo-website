"""Static regression checks; does not start a browser or send a booking."""
import re
import subprocess
import unittest
from pathlib import Path

from bs4 import BeautifulSoup
from scripts.normalize_booking_semantics import semantics

ROOT = Path(__file__).resolve().parent.parent


class BookingSemanticsTests(unittest.TestCase):
    def test_all_220_tracked_heads_have_early_first_charset(self):
        files = subprocess.check_output(["git", "ls-files", "*.html"], cwd=ROOT, text=True).splitlines()
        self.assertEqual(len(files), 220)
        for filename in files:
            source = (ROOT / filename).read_bytes()
            self.assertRegex(source, rb'<head\b[^>]*>\s*<meta charset="utf-8">', filename)
            self.assertLess(source.index(b'<meta charset="utf-8">'), 1024, filename)
            self.assertEqual(len(re.findall(rb'<meta\b[^>]*charset=', source, re.I)), 1, filename)

    def test_widget_labels_errors_and_real_listbox_references(self):
        for filename in ["index.html", "booking.html", "es/booking.html"]:
            soup = BeautifulSoup((ROOT / filename).read_text(), "html.parser")
            home = filename == "index.html"
            form = soup.find(id="booking-widget" if home else "bookingDetailsForm")
            self.assertEqual(form.name, "form")
            self.assertEqual(form.get("toolname"), "prepare_limo_quote")
            self.assertFalse(form.has_attr("toolautosubmit"))
            self.assertIsNone(form.find("form"), filename)
            self.assertTrue(all(b.get("type") == "button" for b in form.find_all("button")))
            for id_ in (["pickup-input", "dropoff-input"] if home else ["pickupInput", "dropoffInput"]):
                field = soup.find(id=id_)
                self.assertEqual(field.get("role"), "combobox")
                self.assertIsNotNone(soup.find("label", attrs={"for": id_}))
                listbox = soup.find(id=field["aria-controls"])
                self.assertIsNotNone(listbox)
                self.assertEqual(listbox.get("role"), "listbox")
                for error_id in field.get("aria-describedby", "").split():
                    error = soup.find(id=error_id)
                    self.assertIsNotNone(error)
                    self.assertTrue(error.has_attr("aria-live") or error.get("role") == "alert")
            if home:
                self.assertIsNotNone(soup.find("label", attrs={"for": "quote-name"}))
                self.assertEqual(soup.find(id="quote-name").get("autocomplete"), "name")
            else:
                for id_ in ["pickupInput", "dropoffInput", "dateInput", "timeHour", "timeMin", "timeAmpm"]:
                    self.assertEqual(soup.find(id=id_).get("form"), "bookingDetailsForm")

    def test_accessibility_changes_preserve_all_existing_inline_styles_and_copy(self):
        for filename in ["index.html", "booking.html", "es/booking.html"]:
            before = subprocess.check_output(["git", "show", "HEAD:" + filename], cwd=ROOT, text=True)
            # Test this migration in isolation: the separate performance build
            # may legitimately relocate styles without changing their appearance.
            after = semantics(before)
            # The only new styled nodes are two display:none listbox references.
            after = re.sub(r'<ul id="(?:pickup|dropoff)-input-google-places"[^>]*></ul>', "", after)
            # No style rewriting or visible copy changes are part of this task.
            for pattern in [r"<style\b[^>]*>([\s\S]*?)</style>", r'\bstyle="([^"]*)"']:
                self.assertEqual(re.findall(pattern, before), re.findall(pattern, after), filename)
            old = BeautifulSoup(before, "html.parser").get_text(" ", strip=True)
            new = BeautifulSoup(after, "html.parser").get_text(" ", strip=True)
            self.assertEqual(old, new, filename)


if __name__ == "__main__":
    unittest.main()
