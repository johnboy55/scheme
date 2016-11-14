# scheme

While doing a phone screen a candidate mentioned one of their projects was a scheme interpreter.

I thought that might be pretty easy, so in a few evenings of hacking, I came up with this. I didn't look at the actual scheme spec, so I kinda made a scheme-like language. But you can write pow in it. 

Functions:

* Arithmatic: +, -, * (no /, % yet)
* Comparison: <, >, =
* Flow: if, list
*  Assignment: lambda, set
   

Types: int, string, function, list

Example
```
    17> (set fib (lambda x (if (< x 2) 1 (+ (fib (- x 1) ) (fib (- x 2) ) ) ) ) )
    18> (set foo (lambda x (if (= x 1) 1 (list (print (fib x)) (foo (- x 1))))))
    19> (foo 5)
```

TODO:
*  It doesn't  support multiple closing )'s for example (+ 2 (* 3 3)), this needs to be (+ 2 (* 3) )
*  It leaks one level of variables into the Global-context in the lambda function. So far I can't see what the effect of this would be, but it doesn't seem to hurt some test cases

  This needs more inline documentation, but seriously, if you're looking for a lispy/scheme
