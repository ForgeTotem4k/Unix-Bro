# Unix-Bro
this tool will be very useful in two cases - 1. you are a lazy person 2. you are a newbie and just learning UNIX, so it may be problematic for you to use the console, which is an integral part of the UNIX system.

# Requirments

```
pip install mistralai==0.4.2
pip install colorama
```

# Installing for Linux

```
git clone https://github.com/ForgeTotem4k/Unix-Bro.git
cd Unix-Bro/
pythom -venv env
source env/bin/activate
pip install mistralai==0.4.2
pip install colorama
python UNIXbro.py
```
# Using
```
🔮 UNIX-Bro by forge 
Пишите что сделать (exit — выход)

➜ create file helloworld.py, write a simple calculator on him, and solve 7*3

⌨  Команда: echo "a = int(input('Enter first number: '))\nb = int(input('Enter second number: '))\nprint('Sum:', a + b)\nprint('Difference:', a - b)\nprint('Product:', a * b)\nprint('Quotient:', a / b)" > helloworld.py; python3 helloworld.py; echo "Product: $(($(cat helloworld.py | python3 -s) * 7 * 3))"
Выполнить команду? (y/N): 
```
