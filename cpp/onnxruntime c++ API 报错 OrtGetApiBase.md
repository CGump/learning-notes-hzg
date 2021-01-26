# onnxruntime c++ API 报错 OrtGetApiBase

编译完成onnxruntime的.so库后，使用测试代码如下，加载onnx模型：

```c++
#include <assert.h>
#include <vector>
#include <onnxruntime_cxx_api.h>

int main(int argc, char* argv[]) {
session_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_EXTENDED);
#ifdef _WIN32
	const wchar_t* model_path = L"squeezenet.onnx";
#else
	const char* model_path = "squeezenet.onnx";
#endif
	printf("Using Onnxruntime C++ API\n");
	Ort::Session session(env, model_path, session_options);
	printf("Done!\n");
	return 0;
}
```

编写Makefile文件如下：

```makefile
CC =g++
#

SRCS := $(wildcard test.cpp )

TARGET :=onnxTest

libs:=-lonnxruntime

default:

	$(CC) -g  -Wall -O2 $(libs)  $(SRCS) -o $(TARGET)

```

运行make指令发现编译报错：

```bash
(base) root@hzg:~/hzg/onnx/onnxruntime-linux-x64-1.6.0# make
g++ -g  -Wall -O2 -lonnxruntime  test.cpp -o onnxTest
/tmp/cc7soTi4.o: In function `_GLOBAL__sub_I_main':
/root/hzg/onnx/onnxruntime-linux-x64-1.6.0/include/onnxruntime_cxx_api.h:71: undefined reference to `OrtGetApiBase'
collect2: error: ld returned 1 exit status
Makefile:12: recipe for target 'default' failed
make: *** [default] Error 1
```

经查询后发现，这其实是编译顺序问题，在编译时先引用了`-lonnxruntime`库，再进行cpp源码的编译，因此，需要更改顺序：

`g++ -g  -Wall -O2 test.cpp -o onnxTest  -lonnxruntime `

此时即可编译成功！

