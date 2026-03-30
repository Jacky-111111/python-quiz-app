# Reflection

1. How far did the agent get?
- It fully implemented my spec. The initial quiz app runs smoothly. Overall, it had 9 Passes, 4 Warns, and 1 Fail under the review of another AI agent. The only Fail lies on security concern associated with pickle. The Warns are mainly at code cleaness and data integrity. Those problems are quickly fixed later. 

2. Where did you intervene?
- I didn't intervene at all during Phase 2. The GPT-5.3 Codex model in Cursor just built everything smoothly from the SPEC.md in one try. I did manually write the credit section after the build (which I forgot to write in the SPEC).

3. How useful was the AI review?
- I'd say it's really useful. It caught bugs that I hadn't thought of testing. It also pointed out concerns involving things I hadn't learned about yet, such as "Data integrity issue: corrupted `.dat` files are silently overwritten, causing potential data loss." I would trust AI review to a large extent from now on.

4. Spec quality → output quality: In hindsight, what would you change about your spec to get a better result from the agent?
- I would provide the exact "graphic-terminal-drawing" for the 112 Dragon in the SPEC, since it didn't do a great job creating it on its own this time. Plus, in the future, I would mention the credits in the SPEC, so I don't have to add it manually. 

5. When would you use this workflow? Based on this experience, when do you think plan-delegate-review is better than conversational back-and-forth? When is it worse?
- I had never written a SPEC.md before, and I had not really thought of error handling or acceptance criteria in my previous coding. This workflow turns out to be very effective in letting AI know what a fully-working app is wanted. At the same time, I also have some doubts. SPEC.md might work well for a terminal-based application, where behavior can be clearly described in words (and the outputs are also in word-contents). However, for a GUI app or a website, it might be harder for AI to interpret and evaluate whether the implementation is correct based only on a written SPEC.md. In that case, more back-and-forth conversation with the AI might be necessary. Plus, when I wanted to add a small feature later (for example, allowing the user to input “goquit” to exit at any time), the most natural and intuitive way for me was to directly tell the agent instead of updating the SPEC. I did not modify the SPEC because I believed that the existing error handling and acceptance criteria would already guide the LLM to properly handle such small additions. For larger structural changes, I think I would go back and modify the SPEC.
