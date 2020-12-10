# Challenge: Voices in the Head (Forensics-2)
We found a voice recording in one of the forensic images but we have no clue what's the voice recording about. Are you able to help?

Hint:
Xiao wants to help. Will you let him help you?

## Summary: 
We were given a .wav file, which we had to go through multiple layers of encoding/steganography to extract the flag

## Process:
All that is included in the file was a wav file, named forensics-challenge-2.wav and the first thing to do is to put it in Audacity to find any obvious messages - which was found immediately when looking at the files spectrogram. It seems to be gibberish, but it ends with a “=” which means it was encoded using Base64 encoding. 

![for-1](https://github.com/BunchOfBytes/STF-2020/blob/main/Forensics/foren1.png)

![for-2](https://github.com/BunchOfBytes/STF-2020/blob/main/Forensics/foren2.png)

We used an online decoder to obtain a pastebin link which gave us this string of random characters

`````````
++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>>++++++++++++++++.------------.+.++++++++++.----------.++++++++++.-----.+.+++++..------------.---.+.++++++.-----------.++++++.
`````````

None of us recognized this weird code, but we identified that there were 8 different characters used, and simple Google searches led us to the “Brainf***” programming language, we then placed this in an online interpreter found here - https://copy.sh/brainfuck/.

`````````
thisisnottheflag
`````````

We bought the hint which said “If you want to keep a secret you must also hide it from yourself”. This means that we missed something along the way but we were still unable to figure it out. After another hint was added which said “Xiao wants to help. Will you let him help you?, we deduced that the ‘Xiao’ the hint was referring to was the Xiao Steganographic Extractor. Using the Xiao Extractor, we extracted a .zip file from the .wav file. The .zip file was password protected. To obtain the password, we used the strings command via the terminal (on macOS) to return all the strings of printable characters within the zip file. Sure enough, we found a string formatted like a flag “govtech-csg{Th1sisn0ty3tthefl@g}” as well as the file within the zip file, named “This is it.docx”

![for-3](https://github.com/BunchOfBytes/STF-2020/blob/main/Forensics/foren3.png)

Initially, we thought that this was the final flag and proceeded to submit it, which was rejected. Soon after, we realised that the “flag” was actually the password to the .zip file. Upon extracting the .docx file from the .zip file, it was found to also be password protected. Instinctively, we entered the initial string we obtained, “thisisnottheflag” as the password as it resembled the password to the .zip file. The password was correct and we were able access the .docx file thereafter. The real flag was then obtained after opening the .docx file using Microsoft Word, which was “govtech-csg{3uph0n1ou5_@ud10_ch@ll3ng3}”.

