import "./App.css";
import { useState } from "react";

const LoginForm = (props) => {
    const [userName, setUserName] = useState("");
    const [passWord, setPassWord] = useState("");
    const [userNameError, setUserNameError] = useState("");
    const [passWordError, setPassWordError] = useState("");

    const handleInputChange = (setInput, event) => {
        setInput(event.target.value);
    };

    const handleSubmit = (event) => {
        let isValid = true;
        if ( userName === "" ) {
            setUserNameError("Please enter username");
            isValid = false;
        }
        if ( passWord === "" ) {
            setPassWordError("Please enter password");
            isValid = false;
        }
        props.setUserName(userName);
        props.setLoggingIn(false);
        console.log(`UserName: ${userName}`);
        event.preventDefault();
    };

    return (
        <form className="login" name="loginForm" action="/login" method="POST">
            <label htmlFor="username">Username:</label>
            <input
                type="text"
                className="inputField"
                id="username"
                name="username"
                placeholder="Enter Username"
                value={userName}
                onChange={(e) => handleInputChange(setUserName, e)}
                onClick={(e) => {setUserNameError("")}}
            />
            <span>{userNameError}</span>
            <br/>
            <label htmlFor="password">Password:</label>
            <input
                type="password"
                className="inputField"
                id="password"
                name="password"
                minLength="8"
                placeholder="Enter Password"
                value={passWord}
                required
                onChange={(e) => handleInputChange(setPassWord, e)}
                onClick={(e) => {setPassWordError("")}}
            />
            <span>{passWordError}</span>
            <br/>
            <input
                type="submit"
                className="formButton"
                id="signin"
                name="signin"
                value="Sign In"
                required
                onClick={(e) => handleSubmit(e)}
            />
            <input
                type="submit"
                className="formButton"
                id="register"
                name="register"
                value="Register"
                onClick={(e) => handleSubmit(e)}
            />
        </form>
    )
}

export default LoginForm;
