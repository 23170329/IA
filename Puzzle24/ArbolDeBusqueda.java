public class ArbolDeBusqueda {
    private final Nodo raiz;
    private int nodosExpandidos;

    public ArbolDeBusqueda(Nodo raiz) {
        this.raiz = raiz;
    }

    // IDA*
    public Nodo buscarIDAStar(String objetivo, boolean usarManhattan) {
        nodosExpandidos = 0;
        int limite = obtenerHeuristica(raiz.getEstado(), objetivo, usarManhattan);

        while (true) {
            Object resultado = search(raiz, objetivo, limite, usarManhattan);
            if (resultado instanceof Nodo) return (Nodo) resultado;
            if ((int) resultado == Integer.MAX_VALUE) return null;
            limite = (int) resultado;
        }
    }

    private Object search(Nodo actual, String objetivo, int limite, boolean usarManhattan) {
        int h = obtenerHeuristica(actual.getEstado(), objetivo, usarManhattan);
        actual.setCosto(h);
        int f = actual.getF();

        if (f > limite) return f;
        if (actual.getEstado().equals(objetivo)) return actual;

        int min = Integer.MAX_VALUE;
        nodosExpandidos++;

        for (Nodo hijo : actual.generarSucesores()) {
            if (actual.getPadre() != null && hijo.getEstado().equals(actual.getPadre().getEstado())) continue;

            Object res = search(hijo, objetivo, limite, usarManhattan);
            if (res instanceof Nodo) return res;
            if ((int) res < min) min = (int) res;
        }
        return min;
    }

    private int obtenerHeuristica(String e, String o, boolean m) {
        return m ? Puzzle24.calcularManhattan(e, o) : Puzzle24.calcularFueraDeLugar(e, o);
    }

    public int getNodosExpandidos() { return nodosExpandidos; }
}
