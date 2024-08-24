import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";
import { Link, useNavigate } from "react-router-dom";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";

export const Login = () => {
	const { store, actions } = useContext(Context);
	const navigate = useNavigate();
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");

	const handleLogin = async (event) => {
		event.preventDefault();

		const success = await actions.userLogin(email, password);
        if (success) {
            navigate('/private'); // Redirige a la página de usuario al iniciar sesión con éxito
        } else {
            alert("No existe una cuenta con ese e-mail. Por favor, revisa si está correcto o regístrate creando una cuenta.");
        }
	}

	return (
		<div className="text-center mt-5">
			<h1>Login</h1>

			<form className="mx-auto w-50" onSubmit={handleLogin}>
				<input type="email" className="form-control" id="exampleFormControlInput1" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required></input>
				<input type="password" id="inputPassword5" className="form-control" aria-describedby="passwordHelpBlock" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required></input>
				<button type="submit" class="btn btn-primary btn-lg">Login</button>
				<Link to="/signup">
					<button type="btn" class="btn btn-warning btn-lg">Signup</button>
				</Link>
			</form>
		</div>
	);
};
