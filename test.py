import unittest
import json2html
import json

class TestJsonToHtml(unittest.TestCase):


    def test_hard(self):
        input_json = '''[
                {
                    "span.class1#id1.class2":"Title #1",
                    "content": [
                        {
                            "p#pid.pclass":"Example 1<h1>",
                            "header":"header 1"
                        }
                    ]
                },
                {"div":"div 1"}
            ]'''
        reference_output = '''<ul><li><span class="class1 class2" id="id1">Title #1</span><content><ul><li><p class="pclass" id="pid">Example 1&lt;h1&gt;</p><header>header 1</header></li></ul></content></li><li><div>div 1</div></li></ul>'''
        output = json2html.main_output(json.loads(input_json))
        self.assertEqual(output, reference_output)


if __name__ == '__main__':
    unittest.main()
