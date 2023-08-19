# File2QR

Tools for transfering a file via QR codes.
There is a server (program that creates QR codes) and a client (parses and reassembles QR codes).
They speak a common protocol, so you could for example use the React Server with the Python client

## Python client

It should work on Linux (if you install a supported screenshot tool - currently only `scrot` / `grim`) and MacOS.

1. Clone this repository and open a shell in it.
2. If you want to have a `qr2file` script for this application, install it with pip:
    ```bash
    pip install ./python-client/
    ```

    Otherwise just install the dependencies:
    ```bash
    pip install -r ./python-client/requirements.in
    ```
3. Run the client.
    If installed with pip you can use `qr2file`.
    You can also always manually call the script:
    ```bash
    python ./python-client/src/main.py -o ~/Downloads
    ```

## Python server

A small single file tools, so that you could transfer it via `xdotool type`.
It should work on Linux systems.
It relies on `qrencode` for actually creating the QR codes, so you may need to install that tool.

Usage:
```bash
./qrencode-server.py /path/to/file
```

Use the `--help` flag to see some performance tweaking options (QR code size and delay between codes).


## React server

You can either self host it, or use the version deployed via Vercel at [react-file2qr.vercel.app](https://react-file2qr.vercel.app/?lang=en).
It should work cross platform with any modern browser (but probably not with Internet Explorer).

## Protocol

Not documented yet, but look at `qrencode-server.py` to understand it.
If you create a client in a different language feel free to open a PR to add the code to this repo, or at least to link to your project :)

## Debugging QR code

[Qr2clipboard](https://gitlab.com/six-two/bin/-/blob/main/general/copy-qr-code) and then:
```
xclip -o -selection clipboard -rmlastnl | base64 -d | hexdump -C | less
```



## Webapp: Available Scripts

The project in `react-server` was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).
