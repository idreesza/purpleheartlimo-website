#!/usr/bin/env python3
"""Repeatable, source-preserving charset and booking semantics migration.

Does not serialize HTML, touch pricing, or change visible text/styles.
"""
import re
import subprocess
from html import escape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
FIELDS = {
    "pickup-input": ("pickup", "Pickup address, airport or hotel"),
    "dropoff-input": ("dropoff", "Drop-off address, airport or hotel"),
    "date-input": ("date", "Pickup date in MM/DD/YYYY"),
    "time-hour": ("hour", "Pickup hour, 1 through 12"),
    "time-min": ("minute", "Pickup minute, 00 through 55 in five-minute increments"),
    "time-ampm": ("ampm", "AM or PM"),
    "quote-name": ("name", "Customer full name"),
    "quote-phone": ("phone", "Customer phone number including area code"),
    "quote-email": ("email", "Optional customer email address"),
    "pax-input": ("passengers", "Passenger count or group range supported by the selected vehicle"),
    "vehicle-input": ("vehicle", "Vehicle: Luxury SUV, Business SUV, Luxury Sedan, Business Sedan, Sprinter Van, Sprinter Jet, Stretch Sedan, Stretch SUV, Party Bus, Coach Bus"),
    "flight-input": ("flight", "Optional flight number"),
    "quote-notes": ("notes", "Optional special requests"),
    "pickupInput": ("pickup", "Pickup address, airport or hotel"),
    "dropoffInput": ("dropoff", "Drop-off address, airport or hotel"),
    "dateInput": ("date", "Pickup date in YYYY-MM-DD"),
    "timeHour": ("hour", "Pickup hour, 1 through 12"),
    "timeMin": ("minute", "Pickup minute: 00, 15, 30 or 45"),
    "timeAmpm": ("ampm", "AM or PM"),
    "fname": ("first_name", "Customer first name"),
    "lname": ("last_name", "Customer last name"),
    "fphone": ("phone", "Customer phone number including area code"),
    "femail": ("email", "Optional customer email address"),
    "fpax": ("passengers", "Passenger count or group range supported by the selected vehicle"),
    "flightInput": ("flight", "Optional flight number"),
    "fmessage": ("message", "Optional special requests"),
    "hourEndDate": ("end_date", "Hourly charter end date in YYYY-MM-DD"),
    "hourEndTime": ("end_time", "Hourly charter end time in HH:MM"),
}
ERRORS = {"pickup-input": "err-pickup", "dropoff-input": "err-dropoff",
          "quote-name": "err-name", "quote-phone": "err-phone"}


class Nodes(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text = text
        self.lines = [0]
        self.lines.extend(m.end() for m in re.finditer("\n", text))
        self.nodes, self.stack = [], []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        start = self.lines[self.getpos()[0] - 1] + self.getpos()[1]
        node = {"tag": tag, "attrs": dict(attrs), "start": start,
                "end": start + len(self.get_starttag_text()),
                "parent": self.stack[-1] if self.stack else None}
        self.nodes.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.stack.pop()

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                node = self.stack[i]
                node["close"] = self.lines[self.getpos()[0] - 1] + self.getpos()[1]
                del self.stack[i:]
                break


def attrs(raw, additions):
    for key, value in additions.items():
        pattern = r"\s" + re.escape(key) + r"""(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+))?(?=[\s/>])"""
        raw = re.sub(pattern, "", raw, flags=re.I)
        at = raw.rfind("/>") if raw.endswith("/>") else raw.rfind(">")
        raw = raw[:at] + ' ' + key + '="' + escape(value, quote=True) + '"' + raw[at:]
    return raw


def semantics(text):
    tree = Nodes(text)
    changes = {}
    by_id = {n["attrs"]["id"]: n for n in tree.nodes if n["attrs"].get("id")}
    widget = by_id.get("booking-widget")
    standalone = "bookingDetailsForm" in by_id

    def change(n, additions):
        key = (n["start"], n["end"])
        changes[key] = attrs(changes.get(key, text[key[0]:key[1]]), additions)

    if widget and widget["tag"] == "div":
        key = (widget["start"], widget["end"])
        changes[key] = text[key[0]:key[1]].replace("<div", "<form", 1)
        end = widget["close"]
        changes[(end, end + len("</div>"))] = "</form>"
    form = widget or by_id.get("bookingDetailsForm")
    if form:
        change(form, {"novalidate": "", "toolname": "prepare_limo_quote",
                      "tooldescription": "Prepare a Purple Heart Limo quote for user review. Fill trip and contact details; the user must click the existing booking button to send a request.",
                      "onsubmit": "event.preventDefault()"})
    for n in tree.nodes:
        a = n["attrs"]
        id_ = a.get("id", "")
        if n["tag"] == "button" and "type" not in a:
            change(n, {"type": "button"})
        if id_ in ERRORS.values() or (id_.startswith("err-")) or id_ in {"alertError", "mdlEditError", "bookingModalError"}:
            change(n, {"aria-live": "polite", "aria-atomic": "true"})
        if id_ not in FIELDS:
            continue
        name, description = FIELDS[id_]
        addition = {"name": name, "toolparamdescription": description}
        if standalone:
            addition["form"] = "bookingDetailsForm"
        if id_ in ERRORS:
            addition["aria-describedby"] = " ".join(dict.fromkeys((a.get("aria-describedby", "") + " " + ERRORS[id_]).split()))
        if id_ in {"fname", "lname", "fphone", "femail", "pickupInput", "dropoffInput"}:
            addition["aria-describedby"] = "alertError"
        if id_ in {"pickup-input", "dropoff-input", "pickupInput", "dropoffInput"}:
            list_id = {"pickupInput": "pickupAc", "dropoffInput": "dropoffAc"}.get(id_, id_ + "-google-places")
            addition.update({"role": "combobox", "aria-autocomplete": "list",
                             "aria-controls": list_id, "aria-expanded": "false"})
            if list_id in by_id:
                change(by_id[list_id], {"role": "listbox", "aria-label": description})
            else:
                # Fixed-position autocomplete reuses this hidden listbox; no layout footprint.
                changes[(n["end"], n["end"])] = '<ul id="' + list_id + '" role="listbox" aria-label="' + escape(description) + '" style="display:none"></ul>'
        if id_ == "quote-name":
            addition["autocomplete"] = "name"
        if id_ == "quote-phone":
            addition["autocomplete"] = "tel"
        if id_ == "quote-email":
            addition["autocomplete"] = "email"
        # Associate the existing visible label, without changing any text.
        parent = n["parent"]
        label = None
        while parent:
            labels = [x for x in tree.nodes if x["tag"] == "label" and x["parent"] is parent]
            if labels:
                label = labels[0]
                break
            if parent is form:
                break
            parent = parent["parent"]
        if label:
            change(label, {"for": id_})
        else:
            addition["aria-label"] = description
        change(n, addition)
    # Accessible names on the actual visible custom controls, not only hidden inputs.
    for n in tree.nodes:
        id_ = n["attrs"].get("id", "")
        if id_.startswith("csel-") or id_ in {"dateCdd", "hourCdd", "minCdd", "ampmCdd", "paxCdd"}:
            field = next((x for x in tree.nodes if x["tag"] == "input" and x["parent"] is n), None)
            if field:
                description = FIELDS.get(field["attrs"].get("id"), ("", field["attrs"].get("id", "")))[1]
                for button in tree.nodes:
                    if button["tag"] == "button" and button["parent"] is n:
                        change(button, {"aria-label": description})
                if n["attrs"].get("class", "").startswith(("cdd", "cdate")):
                    change(n, {"aria-label": description})
    for (start, end), replacement in sorted(changes.items(), reverse=True):
        text = text[:start] + replacement + text[end:]
    if "/js/webmcp-tools.js" not in text:
        text = text.replace("</head>", '<script src="/js/webmcp-tools.js" defer></script>\n</head>', 1)
    return text


def main():
    files = subprocess.check_output(["git", "ls-files", "*.html"], cwd=ROOT, text=True).splitlines()
    changed = []
    for filename in files:
        path = ROOT / filename
        text = path.read_text()
        updated = re.sub(r'<meta\b[^>]*\bcharset\s*=[^>]*>\s*', "", text, flags=re.I)
        updated = re.sub(r'(<head\b[^>]*>)', r'\1\n<meta charset="utf-8">', updated, count=1, flags=re.I)
        if filename in {"index.html", "booking.html", "es/booking.html"}:
            updated = semantics(updated)
        if updated != text:
            path.write_text(updated)
            changed.append(filename)
    print("Updated", len(changed), "HTML files")


if __name__ == "__main__":
    main()
