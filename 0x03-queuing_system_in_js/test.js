const obj = {
  value: 42,
  getValue: function () {
    return this.value;
  },
};

const getValue = obj.getValue;
console.log(getValue());

const boundGetValue = obj.getValue.bind(obj);
console.log(boundGetValue());
