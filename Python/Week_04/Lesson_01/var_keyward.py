def func(*args, **kwargs):
    print(args)
    print(kwargs)


args_dict = {'m': 1, 'n': 2, 'b': 3}

func(args_dict, m=1, n=2)
func(m=1, n=2)#*接受任意数量的位置参数，并将其打包成元组，任意数量包含0


def func(**kwargs):
    print(kwargs)


func(args_dict)  #错误方式，**将接收到的任意数量的关键字参数打包成名称为kwargs的字典，而不能解包字典参数
#TypeError: func() takes 0 positional arguments but 1 was give
