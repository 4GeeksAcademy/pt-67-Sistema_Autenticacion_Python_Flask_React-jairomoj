import React, { useContext, useEffect } from "react";
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";

export const Private = () => {
	const { store, actions } = useContext(Context);
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('token');

        if (!token) {
            navigate('/');
        }
    }, []);

    const handleCloseSession = () => {
        localStorage.removeItem('token');
        navigate('/');
    }

	return (
		<div className="text-center mt-5">
			<h1>Welcome!</h1>

			<button type="button" class="btn btn-danger btn-lg" onClick={handleCloseSession}>Logout</button>
		</div>
	);
};
