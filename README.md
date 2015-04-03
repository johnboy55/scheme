# scheme

While doing a phone screen a candidate mentioned one of their projects was a scheme interpreter.

I thought that might be pretty easy, so in a few evenings of hacking, I came up with this.

TODO:
  It doesn't  support multiple closing )'s for example (+ 2 (* 3 3)), this needs to be (+ 2 (* 3) )
  It leaks one level of variables into the Global-context in the lambda function. So far I can't see what the 
    effect of this would be, but it doesn't seem to hurt some test cases

