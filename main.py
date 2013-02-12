#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import logging
import json
import xml.etree.ElementTree as ET


from google.appengine.api import urlfetch

jinja_env = jinja2.Environment(autoescape=True, 
                                loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 
                                                                            'templates')))

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    def get(self):
        self.render("index.html")

class CanvasGameHandler(Handler):
    def get(self):
        self.render("canvasgame.html")

class ImageFeedHandler(Handler):
    def get(self):
        feed = self.request.GET['tumblr']
        logging.info(feed)
        result = urlfetch.fetch(url=feed)
        rss_xml = ET.fromstring(result.content)
        items = rss_xml[0].findall('item')
        rss = [ {'title': i[0].text, 'description': i[1].text} for i in items]
        html = ''
        for j in rss:
            html += '<div>' + j['title'] + '</div><div>' + j['description'] + '</div>'
        response = json.dumps(rss)
        self.response.headers.add_header('content-type', 
                'application/json', 
                charset='utf-8')
        self.response.write(response)

app = webapp2.WSGIApplication([
    ('/imagefeed', ImageFeedHandler),
    ('/canvasgame', CanvasGameHandler),
    ('/', MainHandler)
], debug=True)
