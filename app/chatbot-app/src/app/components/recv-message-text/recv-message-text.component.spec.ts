import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecvMessageTextComponent } from './recv-message-text.component';

describe('RecvMessageTextComponent', () => {
  let component: RecvMessageTextComponent;
  let fixture: ComponentFixture<RecvMessageTextComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RecvMessageTextComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RecvMessageTextComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
