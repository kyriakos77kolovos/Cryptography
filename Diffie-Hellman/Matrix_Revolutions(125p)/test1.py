def load_matrix(fname, base):
    data = open(fname, 'r').read().strip()
    rows = [list(map(int, row)) for row in data.splitlines()]
    #rows = [list(map(F, row)) for row in rows]
    #print(rows)
    MSpace = MatrixSpace(base, 150, 150)
    return sage.matrix.matrix_generic_dense.Matrix_generic_dense(MSpace, rows, True, True)

def get_identity(v, base):
    MSpace = MatrixSpace(base, 150, 150)
    rows = []
    for i in range(150):
        zeros = [0 for _ in range(150)]
        zeros[i] = v
        rows.append(zeros)
    return sage.matrix.matrix_generic_dense.Matrix_generic_dense(MSpace, rows, True, True)


def get_inverse(M, base):
    MI = M.augment(get_identity(1, base)).rref()
    MI = MI.submatrix(0, 150, 150, 150)
    return MI

def ktheigen(M, k):
    Mroots = M.charpoly().roots()
    count = 0
    last = None
    for v, n in Mroots:
        if count > k:
            break
        last = v
        count += n
    return last

def eigenvectors(M, ev, base):
    Meig = M - get_identity(ev, base)
    v = []
    # Etest = Mext - get_identity(ktheigen(Mext, z))
    Etestec = copy(Meig.echelon_form())
    for i in range(149):
        rv = Etestec.column(150-1)[-i-2]
        rs = Etestec.column(150-i-2)[-i-2]
        Etestec.add_multiple_of_column(150-1, 150-i-2, rv/rs)
        v.insert(0, rv/rs)

    return vector(v + [1])

def random_vector(F):
    v = []
    for i in range(150):
        v.append(F.random_element())
    return v

def get_matrix(rows, base, size=150):
    MSpace = MatrixSpace(base, size, size)
    return sage.matrix.matrix_generic_dense.Matrix_generic_dense(MSpace, rows, True, True)


def basis(w, base):
    vspace = [w] + [[0 for i in range(150)] for _ in range(149)]
    # MSpace = MatrixSpace(GF(2^base), 150, 150)
    M = get_matrix(vspace, base)
    for i in range(149):
        while (True):
            r_v = random_vector(base)
            vspace[i+1] = r_v
            temp = get_matrix(vspace, base)
            if (temp.rank() == i+2):
                # M = M.insert_row(0, r_v)
                break
            print(i)
        print(i)
    return vspace


def transpose(rows, base):
    new_rows = []
    for i in range(150):
        row = []
        for j in range(150):
            row.append(rows[j][i])
        new_rows.append(row)
    return new_rows


def mat_mul(M1, M2, base):
    cols = []
    for i in range(150):
        cols.append(M1*M2.column(i))
    return get_matrix(transpose(cols, base), base)


def to_pari_poly(poly, v):
    pari_poly = ''
    for k in poly.dict().keys():
        pari_poly += f'Mod(1, 2)*{v}^{k}+'

    return pari_poly[:-1]


anss = []
moduli = []
for ii, vv in enumerate([61, 89]):

    M2 = load_matrix('generator.txt', GF(2))

    modulus = M2.charpoly().factor()[ii][0]
    BASIS = GF(2^vv, 'e', modulus=modulus)
    pari_poly = to_pari_poly(modulus, 'x')
    # for k in modulus.dict().keys():
    #     pari_poly += f'Mod(1, 2)*x^{k}+'

    # pari_poly = pari_poly[:-1]

    print(pari_poly)
    print(BASIS)

    M = load_matrix('generator.txt', BASIS)
    A_pub = load_matrix('alice.pub', BASIS)

    print('loaded')
    eigen_vecs = eigenvectors(M, ktheigen(M, 0), BASIS)
    # print(eigen_vecs)
    P = get_matrix(transpose(basis(eigenvectors(M, ktheigen(M, 0), BASIS), BASIS), BASIS), BASIS)
    K = mat_mul(get_inverse(P, BASIS), M, BASIS)
    K = mat_mul(K, P, BASIS)
    KA = mat_mul(get_inverse(P, BASIS), A_pub, BASIS)
    KA = mat_mul(KA, P, BASIS)

    solve = to_pari_poly(KA[0][0].polynomial(), 'g')
    ans = int(pari(f'g = ffgen({pari_poly});fflog({solve}, g)'))
    print(ans)
    anss.append(ans)
    moduli.append(2^ii - 1)

B_pub = load_matrix('bob.pub', GF(2))
print(anss)
A_priv = CRT_list(anss, moduli)
shared_secret = B_pub^A_priv

mat_str = ''.join(str(x) for row in shared_secret for x in row)

open('MAT_STR.txt').write(mat_str)
