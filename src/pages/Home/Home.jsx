import styles from './Home.module.css'
import { ArrowCircleUpLeft, Desktop } from 'phosphor-react'
import LogoCompletaPNG from '../../assets/logo_completa.png'

export default function Home() {
  return (
    <div className={styles.home}>

      <div className={styles.header}>
        <h2 className={styles.textHeader}>FemiBOT ISTs</h2>
        <p>ChatBot de apoio à saúde feminina</p>
      </div>

      <aside className={styles.sidebar}>
        <div className={styles.sidebarContent}>
          <h2 className={styles.sidebarTitle}>Sobre o projeto:</h2>
          <p className={styles.sidebarParagraph}>Apresentamos o novo chatbot de apoio à saúde feminina, especialmente desenvolvido para fornecer informações claras,
             seguras e acessíveis sobre doenças sexualmente transmissíveis (DSTs/ISTs) que afetam as mulheres. Este assistente virtual foi criado para tirar dúvidas,
              orientar sobre prevenção, sintomas, exames e tratamentos, além de indicar quando procurar ajuda médica. Com linguagem acolhedora e sigilosa, o chatbot 
              é uma ferramenta de empoderamento, educação e cuidado com a saúde íntima da mulher.</p>
        </div>

        <footer className={styles.footer}>
          <button className={styles.btnIntegrantes}>
            <a href="/integrantes" className={styles.linkIntegrantes}>
            <ArrowCircleUpLeft size={30} />
            Veja as integrantes do Projeto!
            </a>
          </button>
        </footer>
      </aside>

      

      <div className={styles.buttonsDiv}>
        <h2 className={styles.mainText}>Precisa de ajuda?</h2>
        <button className={styles.btnChat}>
          <a href="/chatbotIST" className={styles.linkChat}>
            <img className={styles.logoCompletaPNG} src={LogoCompletaPNG}></img>
            <p className={styles.textBtn}>Acesse o FemiBOT ISTs!</p>
          </a> 
        </button>
      </div>
      
    </div>
  )
}