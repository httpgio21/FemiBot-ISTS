import React, { useState, useRef, useEffect } from 'react';
import dadosIst from '../../../dadosIst.json';
import { ArrowArcLeft, ArrowClockwise } from 'phosphor-react';
import styles from './ChatBot.module.css';

// Função para limpar texto: remover acentos, pontuação e deixar minúsculo
function limparTexto(texto) {
  return texto
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^\w\s]/gi, '');
}

function identificarTopico(pergunta) {
  const p = limparTexto(pergunta);

  if (p.match(/\b(o que e|oque e|definicao|conceito)\b/)) return 'Definicao';
  if (p.match(/\b(sintoma|sintomas)\b/)) return 'Sintomas';
  if (p.match(/\b(complicacao|complicacoes|problema|problemas|risco)\b/))
    return 'Complicacoes';
  if (p.match(/\b(tratamento|tratar|remedio|cura|medicamento)\b/))
    return 'Tratamento';
  if (p.match(/\b(transmissao|contagio)\b/)) return 'Transmissao';
  if (p.match(/\b(prevencao|prevenir|evitar)\b/)) return 'Prevencao';

  return null;
}

// Flag para recomendar sempre procurar médico
const SEMPRE_RECOMENDAR_MEDICO = true;

function responderPergunta(pergunta) {
  const textoLimpo = limparTexto(pergunta);

  // Verifica se é uma saudação
  if (
    textoLimpo.match(
      /\b(oi|ola|olá|bom dia|boa tarde|boa noite|e ai|fala|hey|hello)\b/
    )
  ) {
    return '👋 Olá! Sou o FemiBOT ISTs, um chatbot especializado em ISTs femininas. Como posso ajudar você hoje?';
  }

  let itemEncontrado = null;

  for (const item of dadosIst) {
    if (textoLimpo.includes(limparTexto(item.Nome))) {
      itemEncontrado = item;
      break;
    }
    for (const chave of item.palavrasChave) {
      if (textoLimpo.includes(limparTexto(chave))) {
        itemEncontrado = item;
        break;
      }
    }
    if (itemEncontrado) break;
  }

  if (!itemEncontrado) {
    return `Desculpe, não consegui identificar sua dúvida. Por favor, mencione o nome da IST ou sintomas específicos.`;
  }

  const topico = identificarTopico(pergunta);

  if (topico) {
    const resposta = itemEncontrado[topico];
    return resposta
      ? `*${itemEncontrado.Nome}* - ${topico.replace('_', ' ')}:\n\n${resposta}` +
        (SEMPRE_RECOMENDAR_MEDICO
          ? `\n\n⚠️ **LEMBRE-SE SEMPRE DE PROCURAR UM MÉDICO PARA DIAGNÓSTICO E TRATAMENTO ADEQUADO.**`
          : '')
      : `Desculpe, não tenho informação sobre "${topico}" para ${itemEncontrado.Nome}.` +
        (SEMPRE_RECOMENDAR_MEDICO
          ? `\n\n⚠️ **LEMBRE-SE SEMPRE DE PROCURAR UM MÉDICO PARA DIAGNÓSTICO E TRATAMENTO ADEQUADO.**`
          : '');
  }

  return (
    `📌 *${itemEncontrado.Nome}*\n\n` +
    `🦠 Sintomas: ${itemEncontrado.Sintomas_em_Mulheres}\n` +
    `⚠️ Complicações: ${itemEncontrado.Complicacoes}\n` +
    `💊 Tratamento: ${itemEncontrado.Tratamento}\n` +
    `🔄 Transmissão: ${itemEncontrado.Transmissao}\n` +
    `✅ Prevenção: ${itemEncontrado.Prevencao}` +
    (SEMPRE_RECOMENDAR_MEDICO
      ? `\n\n⚠️ **LEMBRE-SE SEMPRE DE PROCURAR UM MÉDICO PARA DIAGNÓSTICO E TRATAMENTO ADEQUADO.**`
      : '')
  );
}

export default function ChatBot() {
  const mensagemInicial = {
    remetente: 'bot',
    texto:
      '👋 Olá! Sou o FemiBOT ISTs. Me envie sua dúvida sobre ISTs femininas que eu te ajudo.',
  };

  const [mensagens, setMensagens] = useState([mensagemInicial]);
  const [entrada, setEntrada] = useState('');
  const [carregando, setCarregando] = useState(false);

  const inputRef = useRef(null);
  const containerMensagensRef = useRef(null);

  const enviarMensagem = () => {
    if (!entrada.trim()) return;

    const mensagemUsuario = { remetente: 'usuário', texto: entrada };
    setMensagens((msgs) => [...msgs, mensagemUsuario]);
    setCarregando(true);

    setTimeout(() => {
      const respostaTexto = responderPergunta(entrada);
      const mensagemBot = { remetente: 'bot', texto: respostaTexto };
      setMensagens((msgs) => [...msgs, mensagemBot]);
      setEntrada('');
      setCarregando(false);
    }, 1000);
  };

  const limparChat = () => {
    setMensagens([mensagemInicial]);
    setEntrada('');
  };

  // Foco no input sempre que mensagens atualizam e não está carregando
  useEffect(() => {
    if (!carregando && inputRef.current) {
      inputRef.current.focus();
    }
  }, [carregando, mensagens]);

  // Auto-scroll para o final sempre que mensagens atualizam
  useEffect(() => {
    if (containerMensagensRef.current) {
      containerMensagensRef.current.scrollTop =
        containerMensagensRef.current.scrollHeight;
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
        <a
          href="/"
          className={styles.btnvoltar}
          aria-label="Voltar para a página inicial"
        >
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
          <ArrowClockwise size={28} />
        </button>
      </div>

      <div className={styles.container}>
        <div className={styles.mensagem} ref={containerMensagensRef}>
          {mensagens.map((msg, i) => (
            <div
              key={i}
              className={
                msg.remetente === 'bot'
                  ? styles.mensagemBot
                  : styles.mensagemUser
              }
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
