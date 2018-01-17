<H1> Shared Perspectives for Query by Example in E-Commerce </H1>

Welcome! This is all part of my master thesis at TU Delft, where I try to introduce some _perception-based personalization_ to the process of Query by Example for experience items, such as books and movies, in E-Commerce platforms. This means that users can select an example movie and get similar movies back, but they can choose (to a certain extent) on _why_ the results are similar to the example provided. These experience items are best described by how we perceive them (this book is intense and realistic, or that's a funny and "feel-good" movie), and perception is subjective, so we should be able to select the perception we agree with.

Why do I consider this useful? Well, when we look for experience items like movies or books, most of the times we only know the title of items that what we have already seen or read, or if someone recommended it. But if we want something new for us, we have to explore vast collections of unknown items...where to start? With something that we like! And if we can tune the search by selecting the reason why we liked that item in the first place, we have a better chance of finding something interesting.

For instance, let's say you want to watch something like the Green Mile because it's a good book adaptation with a great story, it doesn't matter if it's very touching and emotional, or if it's a nice and long movie with top-level actors. If you go right now to Netflix or Amazon, trying to find something similar, odds are you'll get any number of T. Hanks movies, along with other movies that people _also_ watched, like Shawshank Redemption. That's great, but not what you're looking for. Furthermore, these systems give no reason behind those similar movies..._it's a secret, man_. Instead, what I'm trying to do is to show 9 similar movies, and tell you "these 3 are similar because they are also touching and emotional, these 3 are also book adaptations with a great story, and these 3 are also long movies with superior cast" (I know, that last example is a bit weird but it's what the prototype actually did ¯\\\_(ツ)\_/¯ ). Then you can decide which way to go, for example Patriot Games is similar because it's also well adapted from a novel and the story is great. It's an action film about spies, not a drama in jail, but it comes from a book!

The challenge with perception is that it is subjective, it varies for everyone and for every item, so it's hard to model it for a database. we can't just decide how people _will_ perceive this book, if players agree that the new gameplay of this videogame is actually engaging, etc. Fortunately, we can find users' perceptions for these items in social media feedback, in particular, we take advantage of user reviews. Users describe their experience with the item, and how they rate those perceptual features I keep talking about:
* This movie is hilarious, I love it -> humor: 10/10
* The story is amazing, the suspense will keep you on the edge of your seat -> story = 9/10, suspense = 8/10  

To extract this features and their values, we can use Natural Language Processing methods, that leverage onthologies, mathematical models, machine learning, deep learning, and many, many other tools. We assume they work well enough for our purpose, and researchers will likely keep working on them and improving their performance, so good for them and for us. We have a numerical representation, or Perceptual Tuple, for every feedback document or review, now what?

The next step is to make sense of hundreds or thousands of Perceptual Tuples for every item. We argue that while every PT represents a single review, not all reviews have a completely individual experience, but they share some common perspective, they are...**Shared Perspectives**! This is the killer feature, we group together similar PTs, instead taking the average or adding all the values for the item into one (like systems do today). If we select a central Tuple from each Shared Perspective, we can use those Shared Perspective Tuples to find movies that were perceived in a similar way by the users, awesome!

The process can be simplified to be quite straightforward, if we can encode user feedback (such as reviews) into Perceptual Tuples(PT), 
and we apply a clustering algorithm on the PTs for every item, we get Shared Perspectives (SPs).
Then the Shared Perspective Tuples, center of those SPs, can be the representation of the item in a Query by Example, 
so a system is able to find the items with most similar experiences by users.
***
Feel free to check the [Wiki](https://github.com/mvallet91/shared-perspectives/wiki) or even the [thesis report](https://repository.tudelft.nl/) for more!

***

**Disclaimer**: The code is not optimal, many for loops could be lambdas, some lists would be better as some special dictionary, etc. But during the processing and implementation I wasn't feeling very adventurous (like using a calculator to do 2+2 in a test, just to be sure). I'll be working on this continuously, maybe you can help too!
