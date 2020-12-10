# Challenge: Only time will tell! (OSINT-6)

This picture was taken sent to us! It seems like a bomb threat! Are you able to tell where and when this photo was taken? This will help the investigating officers to narrow down their search! All we can tell is that it's taken during the day!

For this flag, we require the coordinates as well as when a picture was taken. Gathering the coordinates was easy as it was accessed very quickly through the image’s metadata, requiring us to just check its properties through right clicking the image in Windows, these properties can also be obtained by using exiftool on Mac or Linux. These coordinates were then converted to degrees using the calculator provided in the challenge description.

![](https://github.com/BunchOfBytes/STF-2020/blob/main/Screenshot%20(15).png)

The properties also show the date above, which we thought would be the date the picture was taken. However, the flag govtech-csg{1.285924_103.846835_2020:12:01_1000-1200} was incorrect, which directed our attention to the barcode, which probably held the information we were missing. 

Scanning the barcode directly did not work as the picture was too blurry. Our solution to this was to use Photoshop to sharpen the image, which still did not allow us to scan the image. Thus, we manually recreated the barcode in Google Sheets, which when scanned, gave us “25 October 2020”

![](https://github.com/BunchOfBytes/STF-2020/blob/main/Screenshot%20(18).png)

Finally, we needed the time for when the picture was taken. We used Google Maps to determine the angle the picture was taken from - facing the west, and from there used the shadows cast from the sign to determine the approximate time the picture was taken. As the shadow is pointed in the same direction the Speakers Corner was facing, we determin that it was around noon (10pm-12pm) at that time. So the flag is: govtech-csg{1.285924_103.846835_2020:10:25_1000-1200}

### Flag: govtech-csg{1.285924_103.846835_2020:10:25_1000-1200}
