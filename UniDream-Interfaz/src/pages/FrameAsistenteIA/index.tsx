import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { getUserId } from "../../services/session";
import { resetUserSession } from "../../services/session";
import { chatStream } from "../../services/api";

const userId = getUserId();
// 1. IMPORTAMOS LA FUNCIÓN DEL MESERO (API)

interface Message {
    id: string;
    text: string;
    sender: 'user' | 'bot';
}

export default () => {
    const navigate = useNavigate();
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const textMenuClass = "text-[#0D0D1B] text-sm transition-colors duration-300 hover:text-[#1213ed] active:text-[#1213ed] cursor-pointer font-medium";
    const buttonPressEffect = "transition-transform duration-100 active:scale-95";

    const [inputValue, setInputValue] = useState("");
    // Estado para saber si la IA está pensando
    const [isLoading, setIsLoading] = useState(false); // <--- NUEVO

    const [messages, setMessages] = useState<Message[]>([
        {
            id: crypto.randomUUID(),
            sender: "bot",
            text: "Estoy listo para ayudarte 😊"
        }
    ]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isLoading]); // Agregamos isLoading para que baje cuando aparezca el indicador de carga

    // 2. MODIFICAMOS LA FUNCIÓN DE ENVIAR PARA QUE SEA ASÍNCRONA (ASYNC)
    const handleSendMessage = async () => {
        if (inputValue.trim() === "") return;

        const userText = inputValue;

        const newUserMsg: Message = {
            id: crypto.randomUUID(),
            text: userText,
            sender: "user"
        };

        setMessages(prev => [...prev, newUserMsg]);
        setInputValue("");
        setIsLoading(true);

        // Creamos y agregamos el mensaje del bot vacío
        const botMsg: Message = {
            id: crypto.randomUUID(),
            text: "",
            sender: "bot"
        };
        setMessages(prev => [...prev, botMsg]);

        try {
            await chatStream(userId, userText, (chunk: string) => {
                // Saltar si es el marcador de fin
                if (chunk.includes("[END]")) {
                    setIsLoading(false);
                    return;
                }

                // Actualizamos solo el mensaje del bot con el id correcto
                setMessages(prev => {
                    return prev.map(msg => {
                        if (msg.id === botMsg.id) {
                            return { ...msg, text: msg.text + chunk };
                        }
                        return msg;
                    });
                });
            });

        } catch (error) {
            setMessages(prev => [
                ...prev,
                {
                    id: crypto.randomUUID(),
                    sender: "bot",
                    text: "Error de conexión, intenta de nuevo."
                }
            ]);
        } finally {
            setIsLoading(false);
        }
    };


    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter' && !isLoading) { // Evitamos enviar si ya está cargando
            handleSendMessage();
        }
    };

    return (
        <div className="flex flex-col bg-white min-h-screen">

            {/* --- NAVBAR (IGUAL QUE ANTES) --- */}
            <div className="flex justify-between items-center bg-[#FFFFFFCC] py-4 px-10 sticky top-0 z-50 backdrop-blur-sm shadow-sm">
                <img
                    src={"https://storage.googleapis.com/tagjs-prod.appspot.com/v1/y0WLx2RbqX/549wbqn9_expires_30_days.png"}
                    className="w-[148px] h-[42px] object-contain cursor-pointer"
                    onClick={() => navigate("/")}
                    alt="UniDream Logo"
                />
                <div className="flex-1 flex justify-center items-center gap-12">
                    <span onClick={() => navigate("/")} className={textMenuClass}>{"Inicio"}</span>
                    <span onClick={() => navigate("/carreras")} className={textMenuClass}>{"Carreras"}</span>
                    <span onClick={() => navigate("/universidades")} className={textMenuClass}>{"Universidades"}</span>
                </div>
                <button
                    className={`flex items-center gap-2 bg-[#1313EC] py-2.5 px-6 rounded-full border-0 ${buttonPressEffect}`}
                    style={{ boxShadow: "0px 4px 6px #1313EC33" }}
                    onClick={() => alert("Login presionado")}
                >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-white" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                    </svg>
                    <span className="text-white text-sm font-bold">{"Iniciar Sesión"}</span>
                </button>
            </div>

            {/* --- CHAT --- */}
            <div className="flex-1 flex flex-col items-center py-12 bg-gradient-to-b from-[#AAD5FF] to-[#E7E7F3]">
                <div className="text-center mb-8 px-4">
                    <h1 className="text-gray-900 text-4xl md:text-5xl font-black mb-4">
                        ¿Cuéntame quién eres y <br />quién quieres ser?
                    </h1>
                    <p className="text-gray-700 text-lg max-w-2xl mx-auto font-normal">
                        Tu compañero inteligente para descubrir el profesional que quieres ser.
                    </p>
                </div>

                <div className="flex flex-col w-full max-w-[900px] h-[600px] bg-white rounded-[48px] border border-black overflow-hidden shadow-2xl relative">
                    <div className="flex-1 overflow-y-auto p-8 flex flex-col gap-6">
                        {messages.map((msg) => (
                            <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`flex gap-4 max-w-[80%] ${msg.sender === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                                    {msg.sender === 'bot' && (
                                        <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center shrink-0">
                                            <img src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/y0WLx2RbqX/jh4mpyzd_expires_30_days.png" className="w-8 h-8 object-contain" />
                                        </div>
                                    )}
                                    <div className={`p-4 rounded-2xl text-base leading-relaxed shadow-sm font-normal
                                        ${msg.sender === 'user'
                                            ? 'bg-[#1313EC] text-white rounded-tr-none'
                                            : 'bg-gray-50 text-gray-800 border border-gray-200 rounded-tl-none'
                                        }`}>
                                        {msg.text}
                                    </div>
                                </div>
                            </div>
                        ))}

                        {/* INDICADOR DE CARGA (OPCIONAL PERO RECOMENDADO) */}
                        {isLoading && (
                            <div className="flex justify-start">
                                <div className="flex gap-4 max-w-[80%] flex-row">
                                    <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center shrink-0">
                                        <img src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/y0WLx2RbqX/jh4mpyzd_expires_30_days.png" className="w-8 h-8 object-contain" />
                                    </div>
                                    <div className="p-4 rounded-2xl bg-gray-50 text-gray-500 border border-gray-200 rounded-tl-none italic text-sm">
                                        Escribiendo...
                                    </div>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    <div className="p-6 bg-white border-t border-gray-100">
                        {/* SUGERENCIAS */}
                        <div className="flex gap-2 mb-4 overflow-x-auto pb-2">
                            {["Me interesan las ciencias", "Quiero estudiar Medicina", "Soy bueno en Matemáticas"].map((suggestion, index) => (
                                <button
                                    key={index}
                                    onClick={() => setInputValue(suggestion)}
                                    disabled={isLoading} // Desactivar si está cargando
                                    className="whitespace-nowrap px-4 py-2 rounded-full border border-gray-200 text-xs text-gray-600 hover:bg-gray-50 transition-colors font-medium disabled:opacity-50"
                                >
                                    {suggestion}
                                </button>
                            ))}
                        </div>

                        {/* INPUT AREA */}
                        <div className="flex items-center bg-gray-50 rounded-full border border-gray-300 px-2 py-2 shadow-inner focus-within:ring-2 focus-within:ring-blue-200 transition-all">
                            <input
                                type="text"
                                className="flex-1 bg-transparent border-none outline-none px-4 text-gray-700 placeholder-gray-400 font-normal disabled:opacity-50"
                                placeholder={isLoading ? "Esperando respuesta..." : "Escribe aquí tu consulta..."}
                                value={inputValue}
                                onChange={(e) => setInputValue(e.target.value)}
                                onKeyDown={handleKeyDown}
                                disabled={isLoading} // Bloquear input mientras carga
                            />
                            <button
                                className={`bg-[#1313EC] text-white px-6 py-3 rounded-full font-bold shadow-md hover:bg-[#0f0fb5] transition-colors ${buttonPressEffect} disabled:opacity-50 disabled:cursor-not-allowed`}
                                onClick={handleSendMessage}
                                disabled={isLoading || inputValue.trim() === ""}
                            >
                                {isLoading ? "..." : "Preguntar"}
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* --- FOOTER (IGUAL QUE ANTES) --- */}
            <div className="bg-white py-16 px-20 border-t border-gray-200">
                {/* ... contenido del footer ... */}
                {/* (Omito el footer para ahorrar espacio, déjalo tal cual lo tienes) */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-20 text-[#0D0D1B]">
                    {/* ... */}
                </div>
                <div className="border-t border-gray-200 pt-8 text-center">
                    <span className="text-gray-500 text-sm font-normal">{"© 2026 UniDream Platform. Todos los derechos reservados."}</span>
                </div>
            </div>
        </div>
    )
}