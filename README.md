# gpt-commit
Chatgpt reviewer is your friend!

This repo requires openai's api key to be added to your environment variables.
See: https://platform.openai.com/docs/quickstart/step-2-setup-your-api-key

## Add as command script:
1. Change the path in first_review to correct python path. 
1. Move script to /usr/local/bin
    ```bash
    mv gpt-commit.py /usr/local/bin/gpt-commit
    ```
1. Make script executable
    ```bash
    chmod +x /usr/local/bin/gpt-commit
    ```
1. Add the file location to your .bashrc or .zshrc file:
    ```bash
    export PATH=$PATH:/path/to/gpt-commit
    ```
1. Restart your terminal or run `source ~/.bashrc` or `source ~/.zshrc`
1. Run `gpt-commit <path-to-code-4-review>` in your terminal to see the help message.
