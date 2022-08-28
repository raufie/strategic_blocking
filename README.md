# Systematic Blocker

Ignore the flashy name, The reason for making this is simple. To manage time more simply and force one to work, at the same time keeping track of the data. I keep track of my personal data (like hours worked) and this also serves that purpose... In simple terms this is what this app serves

## Installation

Just get the exe from the dist folder, or from the release option.
Make sure to create a shortcut in windows for the executable. If you use commmand prompt make sure to use it where you intend to save config file (that is if you choose to add it to path, just go for a simpler double click )

Run as an administrator (you'll probably get a warning for icon, which I didn't include anyway)

## Features

### Basic Features

- Manage the time you give to work and make things simpler if anything is overwhelming by starting with 5 minutes
  - Time your work-minutes (minutes you give full attention to something) e.g work for 5 minutes at the start
  - Save the data for your 'focus times'
  - Ability to configure the timing setup (this app uses 3 stage timing procedure [explained next])
  - Notify the user when the time is over
  - Give user the options to move to the next step (don't go automatically)
  - Give user the ability to cancel any 'focus time' whenever they want

### Device Specs

For now this is a command line app on win 10

## The Basics

### config.json

config.json is a must in the installation folder, you must make sure to configure it yourself to your needs

#### path

path is the folder where you wanna store the data.json
if you don't specify it, a data.json will be automatically generated in the current dir of the installation.

#### timer_config

This here is a more important part
The most important part about breaking procrastination is starting, i've observed that just doing work for 5 minutes is enough. If you can fool your brain that is.. after that its easier..

- There are two times you have to describe
- starter_time (in seconds): means the first amount of time you want to give to a task.. by default its 5 minutes
- main_time (in seconds): when you are not overwhelmed by the task at hand, use this option (by default its 30 minutes)
- you would repeat the main time again and again, after each main time you can take a break for whatever amount you like (i take a 10-20 min break it depends on the person that's why I didn't code a timer in (also i'm lazy 😴))

#### So why this?

## Timer app on windows sucks...

They added a timer features on alarm and clocks, but I couldn't customize it.. You can't set your own times.. it's static.
I've been using alarms this whole time and I write the time I focus on a task in my diary, then I take that data and put it in my excel sheets (💀 yeah.. yikes)

I hope it helps someone 💯 thnx for reading
