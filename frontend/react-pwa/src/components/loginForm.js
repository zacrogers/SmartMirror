import React from 'react';


export const LoginForm = () =>{

    return(
        <div>
        <form>
            <label>Username:</label>
            <input type="text" name="username"/>
            <br/>
            <label>Password:</label>
            <input type="password" name="password"/>
            <br/>
            <button>Login</button>
        </form>
        </div>
    )
}
