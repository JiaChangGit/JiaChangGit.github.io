import unittest
from scripts.spec_terms import explain_terms, Reminders

class TermReminderTests(unittest.TestCase):
    def test_first_two_visible_uses_and_independent_editions(self):
        raw='<p>SQ a</p><p>SQ b</p><p>SQ c</p>'
        for lang in ['zh','en']:
            result=explain_terms(raw,'nvme',lang)
            self.assertEqual(result.count('class="st-terms"'),2)
            self.assertTrue(result.endswith('<p>SQ c</p>'))

    def test_ignored_contexts_do_not_consume_reader_uses(self):
        raw='<nav><p>SQ SQ</p></nav><details><summary>SQ</summary><p>SQ SQ</p></details><p>SQ real</p>'
        self.assertEqual(explain_terms(raw,'nvme','zh').count('class="st-terms"'),1)

    def test_preserve_source_and_avoid_substring_matching(self):
        raw='<p>SQE &amp; 0x1234; inactive_NSIS_SQ; MSI-X.</p><p>unrelated</p>'
        result=explain_terms(raw,'nvme','en')
        self.assertIn(raw.split('</p>')[0]+'</p>',result)
        self.assertIn('<dt>SQE</dt>',result)
        self.assertIn('<dt>MSI-X</dt>',result)
        self.assertNotIn('<dt>SQ</dt>',result)
        self.assertNotIn('<dt>MSI</dt>',result)

    def test_existing_visible_definition_is_not_duplicated(self):
        raw='<p>SQ（Submission Queue，提交佇列）</p><p>SQ again</p>'
        result=explain_terms(raw,'nvme','zh')
        self.assertEqual(result.count('class="st-terms"'),1)
        self.assertTrue(result.startswith(raw.split('</p>')[0]+'</p>'))

    def test_svg_text_gets_a_note_outside_the_figure(self):
        raw='<figure><svg><title>SQ</title><desc>SQ</desc><text>SQ</text></svg></figure>'
        result=explain_terms(raw,'nvme','en')
        self.assertTrue(result.startswith(raw))
        self.assertEqual(result.count('<dt>SQ</dt>'),1)

    def test_definition_is_escaped_and_ambiguous_aer_not_guessed(self):
        p=Reminders('<p>X</p>',{'X':('<img>','<img>')},'en')
        self.assertIn('&lt;img&gt;',p.insertions[0][1])
        self.assertEqual(explain_terms('<p>AER SC</p>','nvme','en'),'<p>AER SC</p>')
