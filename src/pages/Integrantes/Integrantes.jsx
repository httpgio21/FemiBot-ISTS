import styles from './Integrantes.module.css';
import GiovanaIntegrante from '../../assets/giovana.jpg'
import RachelIntegrante from '../../assets/rachel.jpg'
import { ArrowArcLeft, ArrowCircleUpLeft } from 'phosphor-react';

export default function Integrantes() {
    return(
        <div className={styles.container}>
            <div className={styles.divTitle}>
                <h3>INTEGRANTES FemiBOT ISTs:</h3>
            </div>

            <div className={styles.divIntegrantes}>
                <div className={styles.integrantes}>
                    <img src='https://upload.wikimedia.org/wikipedia/commons/c/cd/Facebook_logo_%28square%29.png'></img>
                    <h4>Bruna Oliveira</h4>
                </div>

                <div className={styles.integrantes}>
                    <img src='https://upload.wikimedia.org/wikipedia/commons/c/cd/Facebook_logo_%28square%29.png'></img>
                    <h4>Gabriela Duarte</h4>
                </div>

                <div className={styles.integrantes}>
                    <img src={GiovanaIntegrante}></img>
                    <h4>Giovana Amorim</h4>
                </div>

                <div className={styles.integrantes}>
                    <img src={RachelIntegrante}></img>
                    <h4>Rachel Nunes</h4>
                </div>
            </div>

            <footer>
                <button className={styles.button}>
                    <a href="/">
                    <ArrowArcLeft size={20} color="#fff" />
                    Voltar
                    </a>
                </button>
            </footer>

        </div>
    )
}