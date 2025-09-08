# Understanding AI Agents

Repository for AI Agents hands-on workshop

These instructions will guide you through configuring a GitHub Codespaces environment that you can use to run the course labs. 

**1. Click on the button below to start a new codespace from this repository.**

Click here ➡️  [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/skillrepos/ai-agents?quickstart=1)

**2. Then click on the option to create a new codespace.**

![Creating new codespace from button](./images/aa74.png?raw=true "Creating new codespace from button")

This will run for a few minutes while it gets the virtual environment ready. You'll then need to run a setup script to finalize the installation.

**3. Run setup script to finalize the installation.**

In the codespace *TERMINAL* panel at the bottom, run the following command.

```
scripts/setup.sh
```

This will setup the python environment, install needed python pieces, install Ollama, and then download the model we will use. This will take several more minutes to run. 

![Final prep](./images/atoa2.png?raw=true "Final prep")


**4. Open a new terminal.**

When the script is completed (after a long run), you can just click on the "+" sign on the far right to get a new terminal with the provided Python environment to work in.

![New terminal](./images/atoa3.png?raw=true "New terminal")

**5. Open up the *labs.md* file so you can follow along with the labs.**
You can either open it in a separate browser instance or open it in the codespace. 
![Opening labs](./images/aip4.png?raw=true "Opening labs")

**Now, you are ready for the labs!**

**6. (Optional, but recommended) Change your codespace's default timeout from 30 minutes to longer (60 for half-day sessions, 90 for deep dive sessions).**
To do this, when logged in to GitHub, go to https://github.com/settings/codespaces and scroll down on that page until you see the *Default idle timeout* section. Adjust the value as desired.

![Changing codespace idle timeout value](./images/aa4.png?raw=true "Changing codespace idle timeout value")

**NOTE: If your codespace times out and you need to reopen it**

1. Click on the button to restart.
2. Run the *ollama serve &* command to restart Ollama
```
ollama serve &
```

<br/><br/>


