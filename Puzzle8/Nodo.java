import java.util.ArrayList;
import java.util.List;

public class Nodo {

    private String estado;
    private Nodo padre;
    private int nivel;
    private int costo;

    public Nodo(String estado) {
        this.estado = estado;
        this.padre = null;
        this.nivel = 0;
        this.costo = 0;
    }

    public Nodo(String estado, Nodo padre) {
        this.estado = estado;
        this.padre = padre;
        this.nivel = padre.nivel + 1;
        this.costo = 0;
    }

    // Getters
    public String getEstado() {
        return estado;
    }

    public Nodo getPadre() {
        return padre;
    }

    public int getNivel() {
        return nivel;
    }

    public int getCosto() {
        return costo;
    }

    // Setters
    public void setPadre(Nodo padre) {
        this.padre = padre;
    }

    public void setNivel(int nivel) {
        this.nivel = nivel;
    }

    public void setCosto(int costo) {
        this.costo = costo;
    }

    public List<Nodo> generarSucesores() {
        String[] estadosHijos = Puzzle8.generarSucesores(estado);
        List<Nodo> sucesores = new ArrayList<>();

        for (String e : estadosHijos) {
            if (e != null) {
                sucesores.add(new Nodo(e, this));
            }
        }
        return sucesores;
    }
}
