import inspect
import time
import Example
from enum import Enum, auto

import unreal

from Utilities.Utils import Singleton

import Utilities.ChameleonTaskExecutor

import importlib
importlib.reload(Utilities.ChameleonTaskExecutor)


from Utilities.ChameleonTaskExecutor import ChameleonTaskExecutor, get_func_type

class AnotherClass():
    def __init__(self):
        ...

    def instance_fake_task(self, seconds:float):
        print(f"*** AnotherClass instance_fake_task")
        time.sleep(seconds)
        print(f"*** AnotherClass instance_fake_task done, {seconds}s")

    @staticmethod
    def static_fake_task(seconds:float):
        print(f"--- AnotherClass static_fake_task")
        time.sleep(seconds)
        print(f"--- AnotherClass static_fake_task done, {seconds}s")

    @classmethod
    def class_fake_task(cls, seconds: float):
        print(f"=== AnotherClass class_fake_task")
        time.sleep(seconds)
        print(f"=== AnotherClass class_fake_task done, {seconds}s")

    def instance_done(self, future_id:int):
        print(f"*** AnotherClass instance done: {future_id}")

    @staticmethod
    def static_done(future_id:int):
        print(f"--- AnotherClass static_done: {future_id}")

    @classmethod
    def class_done(cls, future_id:int):
        print(f"=== AnotherClass class_done: {future_id}")

class AsyncTaskExample(metaclass=Singleton):
    def __init__(self, json_path:str):
        print("SlowToolTest.__init__ call")
        self.json_path = json_path
        self.data:unreal.ChameleonData = unreal.PythonBPLib.get_chameleon_data(self.json_path)

        self.ui_text_block = "TextBlock"
        self.ui_busy_icon = "BusyIcon"
        self.ui_throbber = "Throbber"
        self.other = AnotherClass()

        self.executor = ChameleonTaskExecutor(self)

    def instance_fake_task(self, seconds:float):
        print(f"*** instance_fake_task")
        time.sleep(seconds)
        print(f"*** instance_fake_task done, {seconds}s")
        return seconds

    @staticmethod
    def static_fake_task(seconds:float):
        print(f"--- static_fake_task")
        time.sleep(seconds)
        print(f"--- static_fake_task done, {seconds}s")

    @classmethod
    def class_fake_task(cls, seconds: float):
        print(f"=== class_fake_task")
        time.sleep(seconds)
        print(f"=== class_fake_task done, {seconds}s")

    def instance_done(self, future_id:int):
        future = self.executor.get_future(future_id)
        result = future.result() if future else None
        print(f"*** instance done: {future_id} result: {result}")
        self.data.set_text(self.ui_text_block, f"instance{future_id}_done{result}")

    @staticmethod
    def static_done(future_id:int):
        print(f"--- static_done: {future_id}")

    @classmethod
    def class_done(cls, future_id:int):
        print(f"=== classmethod: {future_id}")

    def some_func1():
        ...


    def log_func_cmd(self):
        s = ChameleonTaskExecutor.get_cmd_str_from_callable(self.other.instance_done)
        print(s)



    def log_functions(self):
        print("=== self ===")
        print("{} is a {}".format("self.instance_done", get_func_type(self.instance_done)))
        print("{} is a {}".format("self.class_done", get_func_type(self.class_done)))
        print("{} is a {}".format("self.static_done", get_func_type(self.static_done)))

        print("{} is a {}".format("AsyncTaskExample.instance_done", get_func_type(AsyncTaskExample.instance_done)))
        print("{} is a {}".format("AsyncTaskExample.class_done", get_func_type(AsyncTaskExample.class_done)))
        print("{} is a {}".format("AsyncTaskExample.static_done", get_func_type(AsyncTaskExample.static_done)))

        print("{} is a {}".format("staticmethod(self.static_done)", get_func_type(staticmethod(self.static_done))))
        print("{} is a {}".format("lambda o: print(1)", get_func_type(lambda o: print(1))))
        print("{} is a {}".format("AsyncTaskExample.some_func1", get_func_type(AsyncTaskExample.some_func1)))


    def some_slow_tasks(self):
        self.executor.submit_task(self.instance_fake_task, args=[0.5], on_finish_callback=self.instance_done)
        self.executor.submit_task(self.instance_fake_task, args=[1], on_finish_callback=self.other.instance_done)
        self.executor.submit_task(self.instance_fake_task, args=[1.5], on_finish_callback=Example.AsyncTaskExample.AsyncTaskExample.static_done)
        self.executor.submit_task(self.instance_fake_task, args=[2], on_finish_callback=self.class_done)

        self.executor.submit_task(AsyncTaskExample.static_fake_task, args=[2.5], on_finish_callback=self.instance_done)
        self.executor.submit_task(AsyncTaskExample.static_fake_task, args=[3], on_finish_callback=Example.AsyncTaskExample.AsyncTaskExample.static_done)
        self.executor.submit_task(AsyncTaskExample.class_fake_task, args=[3.5], on_finish_callback=Example.AsyncTaskExample.AsyncTaskExample.class_done)

        self.executor.submit_task(AsyncTaskExample.class_fake_task, args=[4], on_finish_callback=self.other.class_done)
        self.executor.submit_task(AsyncTaskExample.class_fake_task, args=[4.5], on_finish_callback=dir)

        self.executor.submit_task(self.other.instance_fake_task, args=[5], on_finish_callback=self.instance_done)
        self.executor.submit_task(self.other.instance_fake_task, args=[5.5], on_finish_callback=self.other.instance_done)



    def on_task_finish(self, future_id:int):
        future = self.executor.get_future(future_id)

        if future is None:
            unreal.log_warning(f"Can't find future: {future_id}")
        else:
            self.data.set_text(self.ui_text_block, f"Done {future.result()}")
            print(f"log Done. Future: {future} id: {future_id} result: {future.result()}")

    def show_busy_info(self):
        self.data.set_text(self.ui_text_block, "Running")
        self.data.set_visibility(self.ui_throbber, "Visible")