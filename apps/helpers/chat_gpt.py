from openai import OpenAI

API_KEY = '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'


class GeneratedAI(object):
    def __init__(self):
        self.api_key = API_KEY

    def client(self):
        return OpenAI(api_key=self.api_key)

    def _make_request(self, prompt):
        try:
            response = self.client().chat.completions.create(
                messages=[
                  
                    {"role": "system", "content": "You are a machine that only returns and replies with valid fixed output format no extra words"},
                    {"role": "user", "content": prompt}
                    
                    ],
                model="gpt-3.5-turbo",
            )
            return response

        except Exception as e:
            return str(e)

    def first(self, review):
        prompt = (
            f"Provide some summaries insight as a proper python JSON response with the following elements based on the company's data reviews below, be carefully respect the key provided below for the JSON response: \n"
            f"- 'summary_title': A summary in English in less than 150 chars. \n"
            f"- 'summary_title_fr': A summary in French in less than 150 chars. In\n"
            f"- 'summary_short': A short summary in English in minimum 700 chars. In"
            f"- 'summary_short_fr': A short summary in French  in minimum 700 chars. \n"
            f"- 'summary_long': A detailed summary in English in minimum 2500 chars. \n"
            f"- 'summary_long_fr': A detailed summary in French in minimum 2500 chars. \n"
            f"- 'bad_than_previous': A boolean value indicating whether the current summary is good \n"
            f"summary_title: if data reviews is less than 2 000 chars only return a JSON displaying not enough data message\n"
            f"summary_title_fr: if data reviews is less than 2 000 chars only return a JSON displaying not enough data message in French\n"
            f"data_reviews: {review}"
        )
        return self._make_request(prompt)

    def onwards(self, prev_description, review):
        prompt = (
            f"Provide some summaries insight as a proper python JSON response with the following elements based on the company's data reviews below, be carefully respect the key provided below for the JSON response: \n"
            f"- 'summary_title': A summary in English in less than 150 chars. \n"
            f"- 'summary_title_fr': A summary in French in less than 150 chars. In\n"
            f"- 'summary_short': A short summary in English in minimum 700 chars. In"
            f"- 'summary_short_fr': A short summary in French  in minimum 700 chars. \n"
            f"- 'summary_long': A detailed summary in English in minimum 2500 chars. \n"
            f"- 'summary_long_fr': A detailed summary in French in minimum 2500 chars. \n"
            f"- 'bad_than_previous': A boolean value indicating whether the current review is better than the previous description \n"
            f"Previous reviews data: {prev_description}\n"
            f"summary_title: if data reviews is less than 2 000 chars only return a JSON displaying not enough data message\n"
            f"summary_title_fr: if data reviews is less than 2 000 chars only return a JSON displaying not enough data message in French\n"
            f"data_reviews: {review}"
        )
        return self._make_request(prompt)

    def translate(self, description):
        prompt = f"Translate to french {description}"
        return self._make_request(prompt)
