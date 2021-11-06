
First plan is make it so that the top N results each print its top M statements using Task 2. Looking at properties and values would help the user select the QID that represents the concept they’re looking for. The other one is using the description at the top of the item page. 	I looked at several descriptions and they were all very good, so we’ll be implementing both discriminators in different functions.

Made a function that returns properties for an item and could work for this, mainly to bridge the gap between functions in task 2 and 3: find a QID, now we can load its data page, but knowing its properties we can print specific statements instead of the whole thing.

So returning to the task, re-reading a lot of stuff, I realized something about the 2 bonuses of Task 3.

Given an article as input, we want to
1. Build a tool that finds potential items to match it with
2. Device a metric that checks how good a match each item is
3. Define a threshold -based on that metric- for when an item can be matched with an article

With these tools, we can return the best matching items for the article and
1. If the article is an unconnected page, match it with the best item if it passes the trheshold
2. If the article already has an item, check if it's the best, change it, or remove it

More or less had an idea of this, what I didn't realize until now is that this is the most open and likely important part of the task. I have some ideas for this although they require time to learn to better implement tools like regex and spaCy.

It's kind of different than the start of the task because the input is not only a concept. So okay, we need to pull valuable info from an article like we did in Task 1. Maybe use some language processing model to automatically get statements like we did manually.

We can use those statements in the API to get good potential data items. We can compare them with the statements of the items, thus getting a matching score. Trying to have one solution for everything is tempting. Multiple ways to extract and process data from an article, both to find good items and to measure matching-ness. Maybe more exploration on the way item statements are displayed in article is needed.
