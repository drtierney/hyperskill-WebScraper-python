import ast
import re

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class WebScraperTest(StageTest):
    def generate(self):
        return [TestCase(stdin="https://www.imdb.com/title/tt10048342/", check_function=self.check_queens_gambit,
                         time_limit=50000),
                TestCase(stdin="https://www.imdb.com/title/tt0068646/", check_function=self.check_godfather,
                         time_limit=50000),
                TestCase(stdin="https://www.imdb.com/name/nm0001191/", check_function=self.check_incorrect_url,
                         time_limit=50000),
                TestCase(stdin="https://www.google.com/", check_function=self.check_incorrect_url, time_limit=50000)]

    def check_incorrect_url(self, reply, attach=None):
        if "Invalid movie page!" in reply:
            return CheckResult.correct()
        else:
            return CheckResult.wrong("""If the link does not contain movie info or not an IMDB resource, 
            please respond with 'Invalid movie page!' message!""")

    def check_queens_gambit(self, reply, attach=None):
        possible_descriptions = ["prodigious introvert Beth Harmon discovers and masters the game of chess"]
        output = re.search('({.+})', reply)
        if output is None:
            return CheckResult.wrong("Output dictionary was expected.\n"
                                     "However, it was not found.")
        try:
            reply_dict = ast.literal_eval(output.group(0))
        except SyntaxError:
            return CheckResult.wrong("An error occurred while your output was being parsed.\n"
                                     "Make sure you output a dictionary and its keys and values contain no HTML tags.")
        except AttributeError:
            return CheckResult.wrong("An error occurred while your output was being parsed.\n"
                                     "Make sure you output a dictionary and its keys and values contain no HTML tags.")
        if 'title' not in reply_dict:
            return CheckResult.wrong("There's no \'title\' field in your output.")
        if 'description' not in reply_dict:
            return CheckResult.wrong("There's no \'description\' field in your output.")
        user_description = reply_dict["description"]
        title = reply_dict["title"]
        if not title or not user_description:
            return CheckResult.wrong("Seems like there is a title or a description missing in the output dictionary.")
        if type(user_description) != str or type(title) != str:
            return CheckResult.wrong("The values of keys 'title' and 'description' should be strings.\n"
                                     "However, it seems that in your output the type of one or both of these values isn't string.")
        correct_descriptions = sum([description.lower().strip() in user_description.lower().strip() for description in possible_descriptions]) > 0
        if "The Queen's Gambit" in title and correct_descriptions:
            return CheckResult.correct()
        else:
            return CheckResult.wrong("Title or description in returned dict do not seem to be correct.")

    def check_godfather(self, reply, attach=None):
        possible_descriptions = ["An organized crime dynasty's aging patriarch transfers control of his clandestine empire to his reluctant son",
                                 "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."]
        output = re.search('({.+})', reply)
        if output is None:
            return CheckResult.wrong("Output dictionary was expected.\n"
                                     "However, it was not found.")
        try:
            reply_dict = ast.literal_eval(output.group(0))
        except SyntaxError:
            return CheckResult.wrong("An error occurred while your output was being parsed.\n"
                                     "Make sure you output a dictionary and its keys and values contain no HTML tags.")
        if 'title' not in reply_dict:
            return CheckResult.wrong("There's no \'title\' field in your output.")
        if 'description' not in reply_dict:
            return CheckResult.wrong("There's no \'description\' field in your output.")
        title = reply_dict.get("title")
        desc = reply_dict.get("description")
        if not title or not desc:
            return CheckResult.wrong("Seems like there is a title or a description missing in the output dictionary.")
        user_description = reply_dict["description"]
        if type(user_description) != str or type(title) != str:
            return CheckResult.wrong("The values of keys 'title' and 'description' should be strings.\n"
                                     "However, it seems that in your output the type of one or both of these values isn't string.")
        correct_descriptions = sum([description.lower().strip() in user_description.lower().strip() for description in possible_descriptions]) > 0
        if "Godfather" in reply_dict["title"] and correct_descriptions:
            return CheckResult.correct()
        else:
            return CheckResult.wrong("Title or description in returned dict do not seem to be correct.")


if __name__ == '__main__':
    WebScraperTest().run_tests()
