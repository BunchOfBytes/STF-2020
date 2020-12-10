# Challenge: Where was he kidnapped? (OSINT-2)
The missing engineer stores his videos from his phone in his private cloud servers. We managed to get hold of these videos and we will need your help to trace back the route taken he took before going missing and identify where he was potentially kidnapped!

## Summary
Players were given 3 video files, they had to trace the postal code of the location of where the videos had taken place.

## Process
This challenge gives us 3 videos. Important information from the videos are first identified. For Video 1, we see Bus Service 117 along with an MRT in the background. With the caption “Finally”, it meant this was the bus service the engineer was waiting for. A quick search here (https://www.transitlink.com.sg/eservice/eguide/service_route.php?service=117) showed that MRT’s at the possible locations of this video were at:

1. Sembawang
	
2. Yishun

3. Khatib

4. Soo Teck

5. Punggol

Using Google Maps, we quickly identified that this was Khatib Station by comparing visual similarities - in particular, the back of a signboard and the colours of the HDB blocks in the back.

![visual similarities](https://github.com/BunchOfBytes/STF-2020/blob/main/Screenshot%20(10).png)

For Video 2, we don’t see much other than two yellow pillars and the caption “Not even near the mrt… such a drag…” meaning that this was his stop and he had just alighted. Following the direction of the MRT and Bus, we know that he is travelling away from Yishun MRT, so we set our location as Khatib MRT and destination as Punggol MRT. (The location where he boarded Bus 117 as well as the terminal Bus 117 was heading to). We used Street View from Google Maps and followed the Bus Route, eventually finding the yellow pillars and confirming the general location of the kidnapping - near the Bus stop Blk 871 (At the Red Circle)

![OSINT-2-1](https://github.com/BunchOfBytes/STF-2020/blob/main/osint-31.png)

Video 3 shows the exact place where the kidnapping happened, which is a void deck area under a HDB block. It is shown in Video 2 that he walked in, meaning that the possible locations were within the area highlighted below. 
![OSINT-2-2](https://github.com/BunchOfBytes/STF-2020/blob/main/osint-32.png)

From here, we just had to use street view further until we found the table and the community garden behind it. (https://www.google.com/maps/@1.4132608,103.8379393,3a,20.8y,75.34h,87.39t/data=!3m7!1e1!3m5!1seW8RJNGwX2BgTjUi3tyBng!2e0!6s%2F%2Fgeo0.ggpht.com%2Fcbk%3Fpanoid%3DeW8RJNGwX2BgTjUi3tyBng%26output%3Dthumbnail%26cb_client%3Dmaps_sv.tactile.gps%26thumb%3D2%26w%3D203%26h%3D100%26yaw%3D177.6653%26pitch%3D0%26thumbfov%3D100!7i16384!8i8192)
![OSINT-2-3](https://github.com/BunchOfBytes/STF-2020/blob/main/osint-33.png)
This area was identified as Block 870. Searching online gave us a postal code of 760870, and indeed govtech-csg{760870} was the flag.

### Flag: govtech-csg{760870}
