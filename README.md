# concurrent-iterator

[![Run Status](https://api.shippable.com/projects/5a9adb0da4261106000330ef/badge?branch=master)](https://app.shippable.com/github/jruere/bounded-iterator)
[![Coverage Badge](https://api.shippable.com/projects/5a9adb0da4261106000330ef/coverageBadge?branch=master)](https://app.shippable.com/github/jruere/bounded-iterator)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/bounded-iterator.svg)](https://pypi.python.org/pypi/bounded-iterator/)
[![License](https://img.shields.io/pypi/l/bounded-iterator.svg)](https://pypi.python.org/pypi/bounded-iterator/)

## Intro

`multiprocessing.pool.ThreadPool` and `multiprocessing.Pool` have the wonderful
`imap` and `imap_unordered` methods which allow to consume an iterable
incrementally and will yield results as they become available.

This is wonderful as it allows to process inputs or results larger than available
memory.

It has an important flaw which is that it does not limit the number of results
that are not consumed. This causes it to use memory without bound.

This package implements a wrapper over an iterable which will limit the number
of results generated until they are acknowledged. It allows a number of
messages to be processed concurrently but no more than that.

## Usage

>> it = itertools.count()           # The input iterable.
>> it = BoundedIterator(10, it)     # Allows concurrent processing of up to 10 values.
>> results = Pool().imap(str, it)   # Will begin consuming `it` and producing results.
>> time.sleep(5)                    # No matter what else we do, no more than 10 results will be available.
>> for res in results:              # Consume normally.
>>   print(res)
>>   it.processed()                 # Acknowledge a value was processed so that a new one can be generated.
