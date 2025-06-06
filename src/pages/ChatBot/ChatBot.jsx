import React, { useState, useRef, useEffect } from 'react';
import { ArrowArcLeft, ArrowClockwise } from 'phosphor-react';
import styles from './ChatBot.module.css';

export default function ChatBot() {
  const mensagemInicial = {
    remetente: 'bot',
    texto: '👋 Olá! Sou o FemiBOT ISTs. Me envie sua dúvida sobre ISTs femininas que eu te ajudo.',
  };

  const [mensagens, setMensagens] = useState([mensagemInicial]);
  const [entrada, setEntrada] = useState('');
  const [carregando, setCarregando] = useState(false);

  const inputRef = useRef(null);
  const containerMensagensRef = useRef(null);

  const enviarMensagem = async () => {
    const entradaNormalizada = entrada.trim();

    if (!entradaNormalizada) return;

    const mensagemUsuario = { remetente: 'usuário', texto: entradaNormalizada };
    setMensagens((msgs) => [...msgs, mensagemUsuario]);
    setCarregando(true);

    try {
      const response = await fetch('http://localhost:8000/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: entradaNormalizada }),
      });

      if (!response.ok) {
        throw new Error('Erro ao acessar o serviço');
      }

      const data = await response.json();
      const mensagemBot = { remetente: 'bot', texto: data.reply };
      setMensagens((msgs) => [...msgs, mensagemBot]);
    } catch (error) {
      const mensagemErro = {
        remetente: 'bot',
        texto: 'Desculpe, ocorreu um erro ao tentar obter a resposta. Tente novamente mais tarde.',
      };
      setMensagens((msgs) => [...msgs, mensagemErro]);
      console.error(error);
    } finally {
      setEntrada('');
      setCarregando(false);
    }
  };

  const limparChat = () => {
    setMensagens([mensagemInicial]);
    setEntrada('');
  };

  useEffect(() => {
    if (!carregando && inputRef.current) {
      inputRef.current.focus();
    }
  }, [carregando, mensagens]);

  useEffect(() => {
    if (containerMensagensRef.current) {
      containerMensagensRef.current.scrollTop = containerMensagensRef.current.scrollHeight;
    }
  }, [mensagens, carregando]);

  const lidarComTeclaPressionada = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      enviarMensagem();
    }
  };

  return (
    <div>
      <div className={styles.header}>
        <a href="/" className={styles.btnvoltar} aria-label="Voltar para a página inicial">
          <ArrowArcLeft size={30} />
        </a>

        <h2 className={styles.textHeader}>FemiBOT ISTs</h2>

        <button
          className={styles.btnRefresh}
          onClick={limparChat}
          aria-label="Limpar chat"
          title="Limpar chat"
          type="button"
          style={{
            background: 'transparent',
            border: 'none',
            cursor: 'pointer',
            marginLeft: 'auto',
            color: '#333',
          }}
        >
          <ArrowClockwise color="white" size={28} />
        </button>
      </div>

      <div className={styles.container}>
        <div className={styles.mensagem} ref={containerMensagensRef}>
          {mensagens.map((msg, i) => (
            <div
              key={i}
              className={msg.remetente === 'bot' ? styles.mensagemBot : styles.mensagemUser}
            >
              <p style={{ whiteSpace: 'pre-line' }}>{msg.texto}</p>
            </div>
          ))}
          {carregando && (
            <div className={styles.mensagemBot}>
              <p>Digitando...</p>
            </div>
          )}
        </div>

        <div className={styles.inputContainer}>
          <input
            ref={inputRef}
            type="text"
            placeholder="Digite sua mensagem..."
            value={entrada}
            onChange={(e) => setEntrada(e.target.value)}
            onKeyDown={lidarComTeclaPressionada}
            disabled={carregando}
          />
          <button type="button" onClick={enviarMensagem} disabled={carregando}>
            {carregando ? 'Enviando...' : 'Enviar'}
          </button>
        </div>
      </div>
    </div>
  );
}
