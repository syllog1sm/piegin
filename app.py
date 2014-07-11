import falcon
import pygal


class ChartResource:
    def on_get(self, req, resp, title, command_str):
        parts = self.parse_command(command_str)
        resp.status = falcon.HTTP_200
        resp.set_header('Content-Type', 'image')
        resp.body = self.make_chart(title, *parts)

    def parse_command(self, command_str):
        strings = command_str.split(',')
        parts = []
        for string in strings:
            name, prob = string.split('..', 1)
            parts.append((name, float(prob)))
        return parts

    def make_chart(self, title, *parts):
        pie_chart = pygal.Pie()
        pie_chart.title = title
        for name, prob in parts:
            pie_chart.add(name, prob)
        return pie_chart.render()


app = falcon.API()

chart = ChartResource()
app.add_route('/!pie/{title}/{command_str}', chart)


if __name__ == '__main__':
    from wsgiref import simple_server

    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
