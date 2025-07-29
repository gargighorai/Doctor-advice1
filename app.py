from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_advice(symptoms):
    symptoms = symptoms.lower()
    if "fever" in symptoms and "cough" in symptoms:
        return "Possible viral infection. Stay hydrated and monitor temperature. Visit a doctor if symptoms persist."
    elif "chest pain" in symptoms:
        return "Chest pain can be serious. Seek immediate medical attention."
    elif "headache" in symptoms:
        return "Try rest and hydration. If severe or persistent, consult a physician."
    else:
        return "Your symptoms need detailed review. Please book a consultation."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    symptoms = request.form['symptoms']
    advice = get_advice(symptoms)
    drugs = ""
    notes = ""

    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    c.execute("INSERT INTO patients (name, age, symptoms, advice, drugs, notes) VALUES (?, ?, ?, ?, ?, ?)",
              (name, age, symptoms, advice, drugs, notes))
    conn.commit()
    conn.close()

    return render_template('result.html', name=name, age=age, symptoms=symptoms, advice=advice)

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    c.execute("SELECT * FROM patients ORDER BY id DESC")
    patients = c.fetchall()
    conn.close()
    return render_template('dashboard.html', patients=patients)

@app.route('/edit/<int:patient_id>', methods=['GET', 'POST'])
def edit_advice(patient_id):
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()

    if request.method == 'POST':
        new_advice = request.form['advice']
        new_drugs = request.form['drugs']
        new_notes = request.form['notes']
        c.execute("UPDATE patients SET advice = ?, drugs = ?, notes = ? WHERE id = ?",
                  (new_advice, new_drugs, new_notes, patient_id))
        conn.commit()
        conn.close()
        return redirect('/dashboard')

    c.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    patient = c.fetchone()
    conn.close()
    return render_template('edit.html', patient=patient)

if __name__ == '__main__':
    app.run(debug=True)
