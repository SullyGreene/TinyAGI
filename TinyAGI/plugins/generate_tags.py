# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/plugins/generate_tags.py

import logging
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from .base_plugin import BasePlugin

logger = logging.getLogger(__name__)

class GenerateTags(BasePlugin):
    def __init__(self, config):
        super().__init__(config)
        self.stopwords = set(stopwords.words('english'))
        self.max_tags = self.config.get('max_tags', 10)

    def execute(self, agent, tool, input_data, options, stream=False):
        text = input_data.get('text', '')
        try:
            tokens = word_tokenize(text)
            filtered_tokens = [word.lower() for word in tokens if word.lower() not in self.stopwords and word.isalpha()]
            freq_dist = nltk.FreqDist(filtered_tokens)
            tags = [word for word, freq in freq_dist.most_common(self.max_tags)]
            logger.info("Generated tags using GenerateTags plugin.")
            return tags
        except Exception as e:
            logger.error(f"Error generating tags: {e}")
            return []


# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
