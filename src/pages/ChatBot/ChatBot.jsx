import React, { useState } from 'react';
import { ArrowArcLeft } from 'phosphor-react';
import styles from './ChatBot.module.css';

export default function ChatBot() {
  const [mensagens, setMensagens] = useState([
    { remetente: 'bot', texto: 'Olá! Sou o FemiBOT ISTs. Me envie sua dúvida sobre ISTs femininas que eu te ajudo.' },
  ]);
  const [entrada, setEntrada] = useState('');
  const [carregando, setCarregando] = useState(false);

  const enviarMensagem = async () => {
    if (!entrada.trim()) return;

    const mensagemUsuario = { remetente: 'usuário', texto: entrada };

    setMensagens((mensagensAnteriores) => [
      ...mensagensAnteriores,
      mensagemUsuario,
    ]);

    setCarregando(true);

    try {
      const resposta = await fetch('http://localhost:8000/mensagem', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ texto: entrada }),
      });

      if (!resposta.ok) {
        throw new Error(`Erro na resposta: ${resposta.statusText}`);
      }

      const dados = await resposta.json();

      const mensagemBot = {
        remetente: 'bot',
        texto: dados.resposta || 'Desculpe, não consegui entender. Tente novamente.',
      };

      setMensagens((mensagensAnteriores) => [
        ...mensagensAnteriores,
        mensagemBot,
      ]);
    } catch (erro) {
      console.error('Erro ao enviar mensagem:', erro);
      setMensagens((mensagensAnteriores) => [
        ...mensagensAnteriores,
        {
          remetente: 'bot',
          texto: '❌ Ops! Houve um erro ao processar sua pergunta. Verifique sua conexão ou tente mais tarde.',
        },
      ]);
    }

    setEntrada('');
    setCarregando(false);
  };

  const lidarComTeclaPressionada = (evento) => {
    if (evento.key === 'Enter') {
      evento.preventDefault();
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
        <p className={styles.textHeader}>ChatBot de apoio à saúde feminina</p>
      </div>

      <div className={styles.container}>
        <div className={styles.mensagem}>
          {mensagens.map((mensagem, indice) => (
            <div
              key={indice}
              className={
                mensagem.remetente === 'bot'
                  ? styles.mensagemBot
                  : styles.mensagemUser
              }
            >
              <p>{mensagem.texto}</p>
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
