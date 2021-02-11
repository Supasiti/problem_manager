from services.path_builder import PathBuilder 
from controllers.top_controller import TopController
from inspect import signature

if __name__ == '__main__':
    # print(PathBuilder().__class__ is PathBuilder)
    # print(PathBuilder.__name__)
    # print(PathBuilder.__class__)
    sig = signature(TopController)

    pos_args = [arg  for arg in sig.parameters.values() if arg.default is arg.empty]
    print(pos_args)


    # sig = signature(PathBuilder)
    # print(len(sig.parameters))