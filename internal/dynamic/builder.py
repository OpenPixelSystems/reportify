'''
@File     :  builder.py
@Desc     :  Dynamic builder class, to generate HTML content for the dynamic reports
@Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
@Date     :  24/12/2023
@Version  :  1.0
@License  :  Copyright (C) 2023 Open Pixel Systems. All rights reserved.
          :  Confidential and for internal use only. The content of this document constitutes proprietary
          :  information of the Open Pixel Systems company. Any disclosure, copying, distribution or use
          :  of any part of the content of this document by unauthorized parties is strictly prohibited.
'''


from internal.builder import Element, Builder


class DynamicBuilder(Builder):
    def build(self, title: str, data: Builder.Data) -> str:
        html = Element('html')
        head = self._head(title, data.test_data)
        body = self._body(title)

        html.add(head)
        html.add(body)

        return self._build(html)

    def _head(self, title: str, test_data: str) -> Element:
        head = Element('head')

        head.add(Element('title', title))
        head.add(Element('link', '',
                         {'rel': 'stylesheet',
                          'href': 'https://fonts.googleapis.com/css?family=Roboto:400,700&display=swap'
                          }))

        styles = self._styles()
        for style in styles:
            head.add(style)

        scripts = self._scripts()
        for script in scripts:
            head.add(script)

        head.add(self._test_data(test_data))

        return head

    def _styles(self) -> list[Element]:
        styles: list[Element] = []

        for style in self.styles:
            styles.append(Element('link', '', {'rel': 'stylesheet', 'href': f'.{style.destination}'}))

        return styles

    def _scripts(self) -> Element:
        scripts: list[Element] = []

        for script in self.scripts:
            scripts.append(Element('script', ' ', {'src': f'.{script.destination}'}))

        return scripts

    def _test_data(self, test_data: str) -> Element:
        return Element('script', f'\n{test_data}\n', {'id': 'test_data', 'type': 'application/json'})

    def _body(self, title: str) -> Element:
        body = Element('body')

        body.add(self._title(title))
        body.add(Element('div', '', {'id': 'content'}))

        return body

    def _title(self, title: str) -> Element:
        return Element('h1', title)
