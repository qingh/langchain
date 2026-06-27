# 总体评价

程序整体没有问题，但有几个需要改进的地方

- 对polyfill概念本身理解不清晰，polyfill无需作为系统函数之外的另一套体系，反而应该和系统函数拥有一样的名称、一样的参数和作用（详见：一般问题-1）
- 对部分Array方法认识有误，建议系统了解map、reduce、filter等方法（详见：一般问题-2、严重问题-1）
- 豆瓣没有完成，请完成后提交



## 严重问题

- `work.js:43`：对reduce的工作过程不清晰，reduce其实是将fn的结果存入临时变量（这里的sum中），而非简单的+=，毕竟，你无法预测用户如何使用你的方法



## 一般问题

- `work.js:7等多处`：此处似乎对polyfill的概念有误解，polyfill不但无需在命名上和系统方法有所区分，恰恰应该和系统函数一致

  - polyfill（可以翻译为修补、填补或填充等）的作用就是在低级浏览器不支持某些系统函数的情况下，为代码提供一致的接口（人话版：在低级浏览器里也能用filter）

  - 所以，此处也应该叫filter，而非filter2，不过，应该注意优先使用系统方法（出于性能考虑）

    > Array.prototype.filter = Array.prototype.filter || function(fn) ...

- `work.js:21`：此处其实无需校验是否是一个json，因为有时也有人用Array.from作为复制一个数组的方法，所以，array本身也是一种可以接受的值

- `work.js:19、25`：null和undefined其实可以合并为一种情况

  > assert(arrayLike, 'invalid array or array-like');



## 建议

- `work.js:39`：此处的逻辑没有问题，但其实可以大幅简化

  ```javascript
  Array.prototype.reduce = Array.prototype.reduce || function(fn, previousValue = 0) {
    assert(typeof fn === 'function', `${fn} is not a function`);
    var sum = previousValue+this[0];
    for (var i = 1; i < this.length; i++) {
      sum=fn(sum, this[i], i, this);
    }
    return sum;
  };
  ```

  









