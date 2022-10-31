# SWACHBIN ![Logo](./images/swachBINLogo.png)
[![License](https://img.shields.io/badge/License-Apache2-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
## Contents
1. [Short Description](#short-description)
1. [Demo Video](#demo-video)
1. [The Architecture](#architecture-overview)
1. [Long Description](#long-description)
1. [Project Roadmap](#project-roadmap)
1. [Addtional Video links](#Additional-video-demo-links)
1. [Built With](#built-with)
1. [The Team](#team)
1. [License](#license)

## Short description 
SwachBIN (inspired from Hindi - swach indicates cleanlines) - a smart AI powered trash bin that solves the waste / trash segregation menace at the source in a seamless way and at the same time accomplishes the task at ultra-low cost and by enabling sustainability.

### What's the problem?
The business case behind this project is that there are many places where community workers manually sort through trash for recycling purposes, such as sorting recycling items from waste items at waste transfer stations before being shipped off. 

Due to rapid urbanisation, the countries like India are facing massive waste management challenge. In India alone over 377 million urban people live in 7,935 towns and cities and generate 62 million tonnes of municipal solid waste per annum but only 43 million tonnes (MT) of the waste is collected, 11.9 MT is treated and 31 MT is dumped in landfill sites[(source)](https://www.downtoearth.org.in/blog/waste/india-s-challenges-in-waste-management-56753). Solid Waste Management (SWM) is one among the basic essential services provided by municipal authorities in the country to keep urban centres clean. However, muncipal bodies are increasingly getting overwhelmed and almost all municipal authorities deposit solid waste at a dumpyard within or outside the city haphazardly. 

One of the key reasons being "segregation at source" is not happening properly. One might ask how about enforcing the law. For instance, in India, various legislations exists for regulating the manner of disposal and dealing with generated waste under the umbrella law of Environment Protection Act, 1986 (EPA) but still landfills are getting dumped with mixed waste a lot leading to pollution.

No matter how strict the laws are there until unless the citizens across the social strata are educated properly on how to deal with generated waste, laws and legislations will exist only in paper.

In simple words, the problem that we have in our hand is - "Not able to segregate waste at source" 
### The idea
The idea is to build a smart trash bin which identifies and detect the trash and perform classification based on AI machine learning algorithms. 
It automatically detect the waste as either recycle or non recycle trash and open the trash can accordingly. It is installed on Raspberry PI and is connected to a camera that take a picture of the trash. With the help of state of the art AI and ML algorithms, the system predicts the trash and classifies the image accordingly, based on the result, an electrical signal is given to the servo motor to rotate which in turn opens the trashcan lid either to left or right depending on the results of recyclable or non recyclable.

Through our solution, we can automate that process with this smart bin which will prove more efficient than current manual processes. There are currently no products like this in existence that we know of -- there are only standard automated recycling machines, which do not come equipped with an AI solution to classify what goes where, so we think it would be a valuable product to create in order to improve efficiency in our society's waste management system.

Moreover it is affordable due to it's ultra low cost and when manufactured and deployed in enmasse the cost will further come down. 
So our team came up with the following vision: SwachBin - an end to end open-source platform which when installed will:
* Solve the problem of “segregation at source” in a seamless manner 
* Educate the user about the type of waste they are disposing
* Enables compliance with local / regional segregation rules and regulations
* Ultra low cost yet sophisticated
* Aligns with UN goal of sustainability 
### How can technology help?
Due to the infusion of AI / ML and advanced HW - it is possible to detect the type of waste source with high accuracy and also through the use of NLP (Text to Speech) we can educate the user as well on the type of waste they are disposing. 
Through our research we found that no solution exits presently that is a combination of highly tech enabled yet highly affordable.

Also thru advanced analytics and IoT platform based dashboard, government bodies can plan their trash picking schedule effectively thus enabling 'reduced carbon emissions'.
- Less trips to households to pick waste = less fuel being burned = reduced carbon emission ..yay :)

## Demo video
[![Watch the video](./images/swachbin_Video_preview_image.jpg)](https://www.youtube.com/)

## Architecture Overview

![Architecture](./images/swachbin_architecture.jpeg)

    1. The waste material / trash is presented in front of the camera that is connected to the SwachBin (powered by Raspberry Pi.)
    2. The captured image of the waste is sent to the Raspberry Pi.
    3. AI Engine at the processes the image and identifies the class of the trash and the category it belongs to. We used Resnet algorithm, winner of multiple algorithm related comepetitions, can have a very deep network of up to 152 layers by learning the residual representation functions instead of learning the signal representation directly.
    4. Depending on the classification, the AI engine sends the corresponding signal to the servo motor, to open the respective lid of the bin.
    5. Classification details are further stored in the SQL database. 
    6. Activity details gets updated in the Docker container.
    7. Depending on the class type of the trash, the LED indicator is turned ON and the speaker conveys the same information as a voice message to the user.
    8. The ultrasonic sensor senses the trash level and sends the information to the flask app to be displayed in the dashboard.
    9. All the information gets displayed in the IoT dashboard.
## Long description
**Key Modules of swachBin:**
1. Hardware based front end
2. AI driven middle ware
3. IoT and SQL infused backend

## Features

## Project roadmap

![Roadmap](./images/swachBin_Roadmap.jpg)

## Built with
![Techonology](./images/tech_logos.jpg)

## Getting started



## Installation


## Additional Video Demo links 


## Team
- [Bharathi Athinarayanan](https://github.com/rathisoft) - _Product owner & AI / ML architect_ 
- [Suneetha Jonnadula](https://github.com/Sunivihaan) - _Lead Full stack developer_
- [Prashanth P](https://github.com/Prashanthp) - _Principal Application developer_
- [Mohamed Fazil](https://github.com/Fazil-24) - _AI / ML Development Engineer_

## License
This project is licensed under the Apache 2 License - see the [LICENSE](LICENSE) file for details.
