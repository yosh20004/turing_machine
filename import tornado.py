import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import os
import test2
import json
import json_test
import dealwithtape
import stack
import _01test



class StackWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        if message == "Update Stack":
            # 当接收到"Update"的消息时，更新栈内容
            self.update_stack()

        elif message == "reset":
            data = test2.clear()
            test2.reset()
            print(data)
            self.write_message(json.dumps(data))

        elif json_test.is_valid_json(message):
            # 当接收到"action"的消息时，执行函数
            data = json_test.check(message)
            test2.clear()
            test2.init(data[1], data[2])
            self.update_stack()


        print(f"Received message from client: {message}") 

    def update_stack(self):
       
        # 在这里更新栈内容，并且发送给客户端
        # [尝试]将update的任务委托给test2去做 test2要重新大改了

        data = test2.update()

        # print(data)
        check = 0
        if (data['state'] == 'trueEND'):
            check = 1
            data = test2.popfunc(data)
            if (test2.output_tape[0] == -1):
                data["state"] = "stop"
            else:
                data["state"] = "success"
        
        # data = {
        #     "stack": l,
        #     "nums": dealwithtape.dealwith_input_tape(test2.curr_list, test2.curr_tar)
        # }

        if data['stack'] == [] and (data['state'] == 'trueEND' or data['state'] == 'stop'):
            data['stack'].append(' ans = {}'.format(test2.output_tape[0]))
  
        self.write_message(json.dumps(data))

        if check == 1:
            print(data['state'])
            try:
                test2.logclass.Map.pop()
            except:
                ...

    def on_close(self):
        print("WebSocket closed")
        test2.clear()
        test2.init_()


    def check_origin(self, origin):
        return True  # 允许跨域请求


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")  # 让Tornado从硬盘上读取html文件并发送至客户端


class StackHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("stack.html")  # 让Tornado从硬盘上读取html文件并发送至客户端


class Stack_push_and_popHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        if message == "pop":
            # 当接收到"Update"的消息时，更新栈内容
            stack.pop()
            self.update_stack()

        elif message == "reset":
            stack.reset()
            self.write_message(json.dumps([]))

        else:
            if message != 'Hello Server':
                stack.push(message)
                self.update_stack()

        print(f"Received message from client: {message}") 
        print(stack.stack)

    def update_stack(self):
        data = {
            "stack": stack.stack,
        }
        self.write_message(json.dumps(data))



class PackbagHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("01packbag.html")  # 让Tornado从硬盘上读取html文件并发送至客户端



class PakWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        _01test.reset()
        _01test.init_()
        print("WebSocket opened")

    def on_message(self, message):
        if message == "Update Stack":
            # 当接收到"Update"的消息时，更新栈内容
            self.update_stack()

        elif message == "reset":
            data = _01test.clear()
            _01test.init_()
            self.write_message(json.dumps(data))

        elif json_test.is_valid_json(message):
            if json_test.is_valid_json(message) == True:
                data = json_test.check_01packbag(message)

                lv = data[1]
                lw = data[2]
                cap = data[3]

                lv = [int(_) for _ in lv]
                lw = [int(_) for _ in lw]

                print(lv, lw, cap)

                if len(lv) != len(lw):
                    print('length not equal')

                else:
                    _01test.clear()
                    _01test.init(lv, lw, cap)
                    self.update_stack()

            # 当接收到"action"的消息时，执行函数
            # print('im here')
            # _01test.clear()
            # _01test.init_()
            # self.update_stack()

        print(f"Received message from client: {message}") 

    def update_stack(self):
       
        # 在这里更新栈内容，并且发送给客户端
        # [尝试]将update的任务委托给test2去做 test2要重新大改了

        data = _01test.update()

        print(data)

        self.write_message(json.dumps(data))

    def on_close(self):
        print("WebSocket closed")
        _01test.clear()


    def check_origin(self, origin):
        return True  # 允许跨域请求    





def make_app():
    return tornado.web.Application([
    (r"/", MainHandler),
    (r"/websocket", StackWebSocketHandler),  # 为Websocket接口添加新的路由/websocket
    (r"/stack", StackHandler),
    (r"/stacksocket", Stack_push_and_popHandler),
    (r"/01packbag", PackbagHandler),
    (r"/01pakwebsocket", PakWebSocketHandler)
    ], 
    static_path=os.path.join(os.path.dirname(__file__), "static")
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8888, address='127.0.0.1')

    test2.init_()

    tornado.ioloop.IOLoop.current().start()


